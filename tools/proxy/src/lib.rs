//! Tirgumim launcher-only proxy DLL.
//!
//! The game loads this DLL from its own folder instead of the System32 one it imports (here
//! `xinput1_3.dll`; the export list comes from `exports/<name>.txt`, every export jumps into the
//! real System32 DLL). It does **nothing** unless the game was started with `TIRGUMIM_LANG=he`
//! or with the argument `-tirgumim_he` (the Tirgumim launcher passes one of them; games that
//! restart themselves through Steam lose environment variables, so those use the argument with
//! `via: "steam"`). A Steam or desktop launch is the original game.
//!
//! With the variable set it reads `<this DLL's folder>\tirgumim\he\redirect.cfg` (or
//! `%TIRGUMIM_DATA_DIR%\redirect.cfg`) and patches the game executable's import table
//! (CreateFileW, GetFileAttributes(Ex)W, FindFirstFile(Ex)W, FindNextFileW, FindClose):
//!   root=..\..\..                     game root, relative to this DLL's folder
//!   add=Ala\Content\Paks\x_P.pak      the game sees this file in that folder (listing, attributes,
//!                                     open); its bytes are <data dir>\x_P.pak. Nothing is written
//!                                     into the game folder.
//!   map=Some\Game\File.bin=File.bin   opening that game file opens <data dir>\File.bin instead
//!   modules=UnityPlayer.dll,kernel32.dll   also patch these modules' import tables. A system DLL here
//!                                     (kernel32.dll, ucrtbase.dll) catches every module's file calls
//!                                     without touching that module: kernel32's CreateFileW & co. are
//!                                     `jmp [IAT]` stubs into kernelbase, so patching kernel32's own
//!                                     import table redirects calls from DLLs we must not hook (FM27's
//!                                     game_plugin.dll); ucrtbase covers CRT fopen. Our hooks call the
//!                                     kernelbase functions directly, so they never re-enter themselves.
//! Missing config or data file: stays inert.
#![allow(non_snake_case, static_mut_refs, clippy::missing_safety_doc)]

use core::ffi::c_void;
use std::collections::HashMap;
use std::sync::Mutex;

include!(concat!(env!("OUT_DIR"), "/stubs.rs"));

type Bool = i32;
type Handle = *mut c_void;
const INVALID: Handle = usize::MAX as Handle;
const MAXP: usize = 32768;

#[repr(C)]
#[derive(Clone, Copy)]
struct FileTime(u32, u32);

#[repr(C)]
struct FindDataW {
    attrs: u32,
    created: FileTime,
    accessed: FileTime,
    written: FileTime,
    size_high: u32,
    size_low: u32,
    reserved0: u32,
    reserved1: u32,
    name: [u16; 260],
    alt: [u16; 14],
}

#[repr(C)]
struct AttrData {
    attrs: u32,
    created: FileTime,
    accessed: FileTime,
    written: FileTime,
    size_high: u32,
    size_low: u32,
}

#[link(name = "kernel32")]
extern "system" {
    fn GetModuleHandleW(name: *const u16) -> Handle;
    fn GetModuleHandleExW(flags: u32, addr: *const c_void, out: *mut Handle) -> Bool;
    fn GetModuleFileNameW(module: Handle, buf: *mut u16, size: u32) -> u32;
    fn VirtualProtect(addr: *mut c_void, size: usize, new: u32, old: *mut u32) -> Bool;
    fn GetSystemDirectoryW(buf: *mut u16, size: u32) -> u32;
    fn LoadLibraryW(name: *const u16) -> Handle;
    fn LoadLibraryExW(name: *const u16, file: Handle, flags: u32) -> Handle;
    fn CreateFile2(p: *const u16, a: u32, s: u32, d: u32, x: *mut c_void) -> Handle;
    fn GetProcAddress(module: Handle, name: *const u8) -> *mut c_void;
    fn GetFullPathNameW(name: *const u16, len: u32, buf: *mut u16, part: *mut *mut u16) -> u32;
    fn GetLastError() -> u32;
    fn SetLastError(e: u32);
    fn CreateFileW(p: *const u16, a: u32, s: u32, sa: *mut c_void, d: u32, f: u32, t: Handle) -> Handle;
    fn GetFileAttributesW(p: *const u16) -> u32;
    fn GetFileAttributesExW(p: *const u16, level: u32, out: *mut c_void) -> Bool;
    fn FindFirstFileW(p: *const u16, out: *mut FindDataW) -> Handle;
    fn FindFirstFileExW(p: *const u16, lvl: u32, out: *mut FindDataW, op: u32, flt: *mut c_void, fl: u32) -> Handle;
    fn FindNextFileW(h: Handle, out: *mut FindDataW) -> Bool;
    fn FindClose(h: Handle) -> Bool;
    fn Sleep(ms: u32);
    fn GetCommandLineW() -> *const u16;
    fn OpenMutexW(access: u32, inherit: Bool, name: *const u16) -> Handle;
    fn CreateMutexW(sa: *mut c_void, owner: Bool, name: *const u16) -> Handle;
    fn CreateThread(sa: *mut c_void, stack: usize, f: extern "system" fn(*mut c_void) -> u32, arg: *mut c_void, fl: u32, id: *mut u32) -> Handle;
}

#[link(name = "shell32")]
extern "system" {
    fn SHGetFolderPathW(hwnd: Handle, csidl: i32, token: Handle, flags: u32, path: *mut u16) -> i32;
}

struct Added {
    dir: String,   // normalized lowercase folder the game sees it in
    name: Vec<u16>, // file name as the game sees it
    lname: String, // lowercase name
    real: Vec<u16>, // NUL-terminated real path
}

struct State {
    maps: HashMap<String, Vec<u16>>, // normalized game path -> NUL-terminated real path
    added: Vec<Added>,
}

static mut STATE: Option<State> = None;

/// The real file functions (kernelbase.dll; fallback: our kernel32 imports), resolved before any patching.
/// Hooks call these, never the kernel32 names: with kernel32's import table patched those lead back here.
struct Real {
    create: usize,
    create2: usize,
    attrs: usize,
    attrs_ex: usize,
    find_first: usize,
    find_first_ex: usize,
    find_next: usize,
    find_close: usize,
}
static mut REAL: Real = Real { create: 0, create2: 0, attrs: 0, attrs_ex: 0, find_first: 0, find_first_ex: 0, find_next: 0, find_close: 0 };

unsafe fn init_real() {
    let kb = GetModuleHandleW(wide("kernelbase.dll").as_ptr());
    let get = |name: &[u8], fallback: usize| {
        let p = if kb.is_null() { core::ptr::null_mut() } else { GetProcAddress(kb, name.as_ptr()) };
        if p.is_null() { fallback } else { p as usize }
    };
    REAL = Real {
        create: get(b"CreateFileW\0", CreateFileW as *const () as usize),
        create2: get(b"CreateFile2\0", CreateFile2 as *const () as usize),
        attrs: get(b"GetFileAttributesW\0", GetFileAttributesW as *const () as usize),
        attrs_ex: get(b"GetFileAttributesExW\0", GetFileAttributesExW as *const () as usize),
        find_first: get(b"FindFirstFileW\0", FindFirstFileW as *const () as usize),
        find_first_ex: get(b"FindFirstFileExW\0", FindFirstFileExW as *const () as usize),
        find_next: get(b"FindNextFileW\0", FindNextFileW as *const () as usize),
        find_close: get(b"FindClose\0", FindClose as *const () as usize),
    };
}

unsafe fn r_create(p: *const u16, a: u32, s: u32, sa: *mut c_void, d: u32, f: u32, t: Handle) -> Handle {
    let f_: unsafe extern "system" fn(*const u16, u32, u32, *mut c_void, u32, u32, Handle) -> Handle = core::mem::transmute(REAL.create);
    f_(p, a, s, sa, d, f, t)
}
unsafe fn r_create2(p: *const u16, a: u32, s: u32, d: u32, x: *mut c_void) -> Handle {
    let f_: unsafe extern "system" fn(*const u16, u32, u32, u32, *mut c_void) -> Handle = core::mem::transmute(REAL.create2);
    f_(p, a, s, d, x)
}
unsafe fn r_attrs(p: *const u16) -> u32 {
    let f_: unsafe extern "system" fn(*const u16) -> u32 = core::mem::transmute(REAL.attrs);
    f_(p)
}
unsafe fn r_attrs_ex(p: *const u16, l: u32, o: *mut c_void) -> Bool {
    let f_: unsafe extern "system" fn(*const u16, u32, *mut c_void) -> Bool = core::mem::transmute(REAL.attrs_ex);
    f_(p, l, o)
}
unsafe fn r_find_first(p: *const u16, o: *mut FindDataW) -> Handle {
    let f_: unsafe extern "system" fn(*const u16, *mut FindDataW) -> Handle = core::mem::transmute(REAL.find_first);
    f_(p, o)
}
unsafe fn r_find_first_ex(p: *const u16, l: u32, o: *mut FindDataW, op: u32, f: *mut c_void, fl: u32) -> Handle {
    let f_: unsafe extern "system" fn(*const u16, u32, *mut FindDataW, u32, *mut c_void, u32) -> Handle = core::mem::transmute(REAL.find_first_ex);
    f_(p, l, o, op, f, fl)
}
unsafe fn r_find_next(h: Handle, o: *mut FindDataW) -> Bool {
    let f_: unsafe extern "system" fn(Handle, *mut FindDataW) -> Bool = core::mem::transmute(REAL.find_next);
    f_(h, o)
}
unsafe fn r_find_close(h: Handle) -> Bool {
    let f_: unsafe extern "system" fn(Handle) -> Bool = core::mem::transmute(REAL.find_close);
    f_(h)
}
static FINDS: Mutex<Option<HashMap<usize, Vec<usize>>>> = Mutex::new(None); // find handle -> pending `added` indexes
static mut DEBUG: bool = false;
static mut MODULES: Vec<Vec<u16>> = Vec::new(); // extra modules to hook (besides the exe), NUL-terminated
static mut NEXT_FAKE: usize = 0x7a11_0000;

fn wide(s: &str) -> Vec<u16> {
    s.encode_utf16().chain(Some(0)).collect()
}

unsafe fn wlen(p: *const u16) -> usize {
    let mut n = 0;
    while *p.add(n) != 0 {
        n += 1;
    }
    n
}

/// Absolute, backslashed, lowercase, without `\\?\`, without trailing backslash.
unsafe fn normalize(p: *const u16) -> Option<String> {
    if p.is_null() {
        return None;
    }
    let mut v: Vec<u16> = core::slice::from_raw_parts(p, wlen(p)).iter().map(|&c| if c == b'/' as u16 { b'\\' as u16 } else { c }).collect();
    let pre: Vec<u16> = "\\\\?\\".encode_utf16().collect();
    if v.starts_with(&pre) {
        v.drain(..4);
    }
    v.push(0);
    let mut buf = vec![0u16; MAXP];
    let n = GetFullPathNameW(v.as_ptr(), MAXP as u32, buf.as_mut_ptr(), core::ptr::null_mut()) as usize;
    if n == 0 || n >= MAXP {
        return None;
    }
    let mut s = String::from_utf16_lossy(&buf[..n]).to_lowercase();
    while s.ends_with('\\') {
        s.pop();
    }
    Some(s)
}

unsafe fn state() -> Option<&'static State> {
    STATE.as_ref()
}

unsafe fn lookup(p: *const u16) -> Option<*const u16> {
    let st = state()?;
    let n = normalize(p)?;
    if let Some(r) = st.maps.get(&n) {
        return Some(r.as_ptr());
    }
    st.added.iter().find(|a| n.len() == a.dir.len() + 1 + a.lname.len() && n.starts_with(&a.dir) && n.ends_with(&a.lname)).map(|a| a.real.as_ptr())
}

unsafe extern "system" fn h_createfilew(p: *const u16, a: u32, s: u32, sa: *mut c_void, d: u32, f: u32, t: Handle) -> Handle {
    let r = lookup(p);
    if r.is_some() {
        log(&format!("open {:?} redirected", normalize(p)));
    }
    r_create(r.unwrap_or(p), a, s, sa, d, f, t)
}
unsafe extern "system" fn h_createfile2(p: *const u16, a: u32, s: u32, d: u32, x: *mut c_void) -> Handle {
    let r = lookup(p);
    if r.is_some() {
        log(&format!("open2 {:?} redirected", normalize(p)));
    }
    r_create2(r.unwrap_or(p), a, s, d, x)
}
unsafe extern "system" fn h_loadlibraryexw(p: *const u16, f: Handle, fl: u32) -> Handle {
    let m = LoadLibraryExW(p, f, fl);
    patch_all(false); // a module we watch may have just been loaded: hook it before it runs
    m
}
unsafe extern "system" fn h_loadlibraryw(p: *const u16) -> Handle {
    let m = LoadLibraryW(p);
    patch_all(false);
    m
}
unsafe extern "system" fn h_getfileattributesw(p: *const u16) -> u32 {
    r_attrs(lookup(p).unwrap_or(p))
}
unsafe extern "system" fn h_getfileattributesexw(p: *const u16, l: u32, o: *mut c_void) -> Bool {
    r_attrs_ex(lookup(p).unwrap_or(p), l, o)
}

/// `*`, `*.*`, `*.ext`, `name*`, exact (case-insensitive). Enough for engine directory scans.
fn wild(pat: &str, name: &str) -> bool {
    if pat == "*" || pat == "*.*" {
        return true;
    }
    match pat.find('*') {
        None => pat == name,
        Some(i) => {
            let (a, b) = (&pat[..i], &pat[i + 1..]);
            !b.contains('*') && name.len() >= a.len() + b.len() && name.starts_with(a) && name.ends_with(b)
        }
    }
}

/// Which `added` files belong in a listing of `pattern` (that don't exist there for real).
unsafe fn injections(pattern: *const u16) -> Vec<usize> {
    let Some(st) = state() else { return vec![] };
    let Some(n) = normalize(pattern) else { return vec![] };
    let Some(cut) = n.rfind('\\') else { return vec![] };
    let (dir, pat) = (&n[..cut], &n[cut + 1..]);
    let mut out = vec![];
    for (i, a) in st.added.iter().enumerate() {
        if a.dir == dir && wild(pat, &a.lname) {
            let mut vis: Vec<u16> = wide(&format!("{dir}\\{}", a.lname));
            vis.pop();
            vis.push(0);
            if r_attrs(vis.as_ptr()) == u32::MAX {
                out.push(i);
            }
        }
    }
    out
}

unsafe fn fill(idx: usize, out: *mut FindDataW) -> bool {
    let Some(st) = state() else { return false };
    let a = &st.added[idx];
    let mut ad: AttrData = core::mem::zeroed();
    if r_attrs_ex(a.real.as_ptr(), 0, &mut ad as *mut _ as *mut c_void) == 0 {
        return false;
    }
    let o = &mut *out;
    o.attrs = ad.attrs;
    o.created = ad.created;
    o.accessed = ad.accessed;
    o.written = ad.written;
    o.size_high = ad.size_high;
    o.size_low = ad.size_low;
    o.reserved0 = 0;
    o.reserved1 = 0;
    o.name = [0; 260];
    let k = a.name.len().min(259);
    o.name[..k].copy_from_slice(&a.name[..k]);
    o.alt = [0; 14];
    true
}

unsafe fn begin_find(h: Handle, pattern: *const u16, out: *mut FindDataW) -> Handle {
    let mut inj = injections(pattern);
    if DEBUG {
        log(&format!("find {:?} -> {} injected", normalize(pattern), inj.len()));
    }
    if inj.is_empty() {
        return h;
    }
    let mut h = h;
    if h == INVALID {
        // the folder has no real match: hand out our entry under a fake handle
        let first = inj.remove(0);
        if !fill(first, out) {
            return INVALID;
        }
        NEXT_FAKE += 4;
        h = NEXT_FAKE as Handle;
    }
    FINDS.lock().unwrap().get_or_insert_with(HashMap::new).insert(h as usize, inj);
    SetLastError(0);
    h
}

unsafe extern "system" fn h_findfirstfilew(p: *const u16, out: *mut FindDataW) -> Handle {
    let h = r_find_first(p, out);
    let e = GetLastError();
    let r = begin_find(h, p, out);
    if r == h && h == INVALID {
        SetLastError(e);
    }
    r
}
unsafe extern "system" fn h_findfirstfileexw(p: *const u16, l: u32, out: *mut FindDataW, op: u32, f: *mut c_void, fl: u32) -> Handle {
    let h = r_find_first_ex(p, l, out, op, f, fl);
    if l != 0 && l != 1 {
        return h;
    }
    let e = GetLastError();
    let r = begin_find(h, p, out);
    if r == h && h == INVALID {
        SetLastError(e);
    }
    r
}
unsafe extern "system" fn h_findnextfilew(h: Handle, out: *mut FindDataW) -> Bool {
    let fake = (h as usize) >= 0x7a11_0000 && (h as usize) < 0x7a12_0000;
    if !fake {
        if r_find_next(h, out) != 0 {
            return 1;
        }
        if GetLastError() != 18 {
            return 0;
        }
    }
    let next = FINDS.lock().unwrap().as_mut().and_then(|m| m.get_mut(&(h as usize)).and_then(|v| if v.is_empty() { None } else { Some(v.remove(0)) }));
    match next {
        Some(i) if fill(i, out) => {
            SetLastError(0);
            1
        }
        _ => {
            SetLastError(18); // ERROR_NO_MORE_FILES
            0
        }
    }
}
unsafe extern "system" fn h_findclose(h: Handle) -> Bool {
    let had = FINDS.lock().unwrap().as_mut().and_then(|m| m.remove(&(h as usize))).is_some();
    if had && (h as usize) >= 0x7a11_0000 && (h as usize) < 0x7a12_0000 {
        return 1;
    }
    r_find_close(h)
}

/// Import-table DLL names whose file functions we hook (kernel32 and its API sets).
fn is_kernel(name: &[u8]) -> bool {
    let n = String::from_utf8_lossy(name).to_ascii_lowercase();
    n == "kernel32.dll" || n == "kernelbase.dll" || n.starts_with("api-ms-win-core-file") || n.starts_with("api-ms-win-core-libraryloader")
}

/// Replace `func` (imported from kernel32 or an API set) in the import table of the module at `base`.
unsafe fn patch_iat(base: *const u8, func: &str, new: usize) -> usize {
    if base.is_null() {
        return 0;
    }
    let rd32 = |off: usize| core::ptr::read_unaligned(base.add(off) as *const u32) as usize;
    let cstr = |p: *const u8| {
        let mut n = 0;
        while *p.add(n) != 0 {
            n += 1;
        }
        core::slice::from_raw_parts(p, n)
    };
    let nt = rd32(0x3c);
    let opt = nt + 24;
    if rd32(nt) != 0x4550 || core::ptr::read_unaligned(base.add(opt) as *const u16) != 0x20b {
        return 0;
    }
    let imp = rd32(opt + 112 + 8);
    if imp == 0 {
        return 0;
    }
    let mut ok = 0;
    let mut d = imp;
    loop {
        let (oft, name, ft) = (rd32(d), rd32(d + 12), rd32(d + 16));
        if name == 0 && ft == 0 {
            break;
        }
        if is_kernel(cstr(base.add(name))) {
            let lookup = if oft != 0 { oft } else { ft };
            let mut i = 0usize;
            loop {
                let ent = core::ptr::read_unaligned(base.add(lookup + i * 8) as *const u64);
                if ent == 0 {
                    break;
                }
                if ent & (1u64 << 63) == 0 && cstr(base.add(ent as usize + 2)) == func.as_bytes() {
                    let slot = base.add(ft + i * 8) as *mut usize;
                    let mut old = 0u32;
                    if core::ptr::read_volatile(slot) != new && VirtualProtect(slot as *mut c_void, 8, 0x04, &mut old) != 0 {
                        core::ptr::write(slot, new);
                        VirtualProtect(slot as *mut c_void, 8, old, &mut old);
                        ok += 1;
                    }
                }
                i += 1;
            }
        }
        d += 20;
    }
    ok
}

unsafe fn own_dir() -> Option<String> {
    let mut me: Handle = core::ptr::null_mut();
    // FROM_ADDRESS | UNCHANGED_REFCOUNT
    if GetModuleHandleExW(4 | 2, own_dir as *const c_void, &mut me) == 0 {
        return None;
    }
    let mut buf = vec![0u16; MAXP];
    let n = GetModuleFileNameW(me, buf.as_mut_ptr(), MAXP as u32) as usize;
    let s = String::from_utf16_lossy(&buf[..n]);
    s.rfind(['\\', '/']).map(|i| s[..i].to_string())
}

/// With TIRGUMIM_DEBUG set, append a line to %TEMP%\tirgumim_proxy.log.
fn log(msg: &str) {
    if !unsafe { DEBUG } {
        return;
    }
    use std::io::Write;
    let p = std::env::temp_dir().join("tirgumim_proxy.log");
    if let Ok(mut f) = std::fs::OpenOptions::new().create(true).append(true).open(p) {
        let _ = writeln!(f, "{msg}");
    }
}

fn env(name: &str) -> Option<String> {
    std::env::var(name).ok().filter(|v| !v.is_empty())
}

/// `{Documents}` / `{LocalAppData}` / `{AppData}` / `{UserProfile}` in config paths.
unsafe fn expand(p: &str) -> String {
    let mut out = p.to_string();
    for (tag, csidl) in [("{Documents}", 0x05), ("{LocalAppData}", 0x1c), ("{AppData}", 0x1a), ("{UserProfile}", 0x28)] {
        if out.contains(tag) {
            let mut buf = vec![0u16; 260];
            if SHGetFolderPathW(core::ptr::null_mut(), csidl, core::ptr::null_mut(), 0, buf.as_mut_ptr()) == 0 {
                let n = wlen(buf.as_ptr());
                out = out.replace(tag, &String::from_utf16_lossy(&buf[..n]));
            }
        }
    }
    out
}

/// Files outside the game folder that the game must see only in Hebrew sessions:
///   place=<target>=<file in data dir>   copied there for the session, removed afterwards
///   swap=<target>=<file in data dir>    the user's file is kept in <data>\orig\ and put back afterwards
///   remove=<target>                     also deleted afterwards (e.g. a cache the game builds from a placed file)
struct Session {
    place: Vec<(String, String)>,
    swap: Vec<(String, String)>,
    remove: Vec<String>,
    orig: String,
}

static mut SESSION: Option<Session> = None;

fn file_name(p: &str) -> &str {
    p.rsplit(['\\', '/']).next().unwrap_or(p)
}

/// Put everything back as it was before a Hebrew session (safe to run any number of times).
unsafe fn restore(se: &Session) {
    for (t, _) in &se.swap {
        let saved = format!("{}\\{}", se.orig, file_name(t));
        if std::path::Path::new(&saved).is_file() && std::fs::copy(&saved, t).is_ok() {
            let _ = std::fs::remove_file(&saved);
            log(&format!("restored {t}"));
        }
    }
    for (t, _) in &se.place {
        if std::fs::remove_file(t).is_ok() {
            log(&format!("removed {t}"));
        }
    }
    for t in &se.remove {
        let _ = std::fs::remove_file(t);
    }
}

unsafe fn begin_session(se: &Session, data: &str) -> bool {
    let _ = std::fs::create_dir_all(&se.orig);
    for (t, f) in &se.swap {
        let saved = format!("{}\\{}", se.orig, file_name(t));
        if !std::path::Path::new(&saved).is_file() && std::path::Path::new(t).is_file() && std::fs::copy(t, &saved).is_err() {
            return false; // could not keep the user's file: leave it alone
        }
        if std::fs::copy(format!("{data}\\{f}"), t).is_err() {
            return false;
        }
    }
    for (t, f) in &se.place {
        if let Some(dir) = std::path::Path::new(t).parent() {
            let _ = std::fs::create_dir_all(dir);
        }
        if std::fs::copy(format!("{data}\\{f}"), t).is_err() {
            return false;
        }
    }
    true
}

unsafe fn activate() {
    let cmd = String::from_utf16_lossy(core::slice::from_raw_parts(GetCommandLineW(), wlen(GetCommandLineW()))).to_lowercase();
    DEBUG = std::env::var_os("TIRGUMIM_DEBUG").is_some() || cmd.contains("-tirgumim_debug");
    let flag = cmd.split_whitespace().any(|a| a == "-tirgumim_he") || env("TIRGUMIM_LANG").is_some_and(|v| v.eq_ignore_ascii_case("he"));
    let Some(dll_dir) = own_dir() else { return };
    let data = env("TIRGUMIM_DATA_DIR").unwrap_or_else(|| format!("{dll_dir}\\tirgumim\\he"));
    let data = data.trim_end_matches(['\\', '/']).to_string();
    let Ok(cfg) = std::fs::read_to_string(format!("{data}\\redirect.cfg")) else { return };
    init_real();
    // Files outside the game folder: first undo whatever an earlier Hebrew session left (crash case),
    // so a launch without the flag is always the original game.
    let mut se = Session { place: vec![], swap: vec![], remove: vec![], orig: format!("{data}\\orig") };
    for line in cfg.lines().map(str::trim) {
        let pair = |r: &str| r.rsplit_once('=').map(|(t, f)| (expand(t), f.to_string()));
        if let Some(p) = line.strip_prefix("place=").and_then(pair) {
            se.place.push(p);
        } else if let Some(p) = line.strip_prefix("swap=").and_then(pair) {
            se.swap.push(p);
        } else if let Some(r) = line.strip_prefix("remove=") {
            se.remove.push(expand(r));
        }
    }
    // Other programs in the game folder (Unity's crash handler...) load this DLL too, without the flag,
    // while a Hebrew session runs: they must not clean up under it.
    let lock = wide("Local\\TirgumimHebrewSession");
    if !flag {
        if OpenMutexW(0x0010_0000, 0, lock.as_ptr()).is_null() {
            restore(&se); // no Hebrew session running: undo anything a crashed one left
        }
        return; // not started by the Tirgumim launcher: original game
    }
    CreateMutexW(core::ptr::null_mut(), 0, lock.as_ptr()); // held until the game exits
    restore(&se);
    log("activate: Hebrew session");
    if !begin_session(&se, &data) {
        restore(&se);
        return;
    }
    SESSION = Some(se);
    let mut root = dll_dir.clone();
    let mut st = State { maps: HashMap::new(), added: vec![] };
    let game = |root: &str, rel: &str| normalize(wide(&format!("{root}\\{rel}")).as_ptr());
    for line in cfg.lines().map(str::trim) {
        if let Some(r) = line.strip_prefix("root=") {
            root = format!("{dll_dir}\\{r}");
        } else if let Some(r) = line.strip_prefix("add=") {
            let real = format!("{data}\\{}", r.rsplit(['\\', '/']).next().unwrap_or(r));
            let Some(n) = game(&root, r) else { continue };
            if !std::path::Path::new(&real).is_file() {
                return; // incomplete install: run the original game
            }
            let cut = n.rfind('\\').unwrap_or(0);
            let shown = r.rsplit(['\\', '/']).next().unwrap_or(r);
            st.added.push(Added { dir: n[..cut].to_string(), name: shown.encode_utf16().collect(), lname: n[cut + 1..].to_string(), real: wide(&real) });
        } else if let Some(r) = line.strip_prefix("modules=") {
            MODULES = r.split(',').map(|m| wide(m.trim())).collect();
        } else if let Some(r) = line.strip_prefix("map=") {
            let Some((g, f)) = r.split_once('=') else { continue };
            let real = format!("{data}\\{f}");
            if !std::path::Path::new(&real).is_file() {
                return;
            }
            if let Some(n) = game(&root, g) {
                st.maps.insert(n, wide(&real));
            }
        }
    }
    if st.maps.is_empty() && st.added.is_empty() {
        return;
    }
    STATE = Some(st);
    patch_all(true);
    // Steam's DRM wrapper fills the import table again after unpacking the game, which undoes our
    // patches. Watch the slots for the first minute and put ours back (engine file I/O starts later).
    extern "system" fn watch(_: *mut c_void) -> u32 {
        unsafe {
            for _ in 0..60000 {
                Sleep(1);
                patch_all(false);
            }
        }
        0
    }
    CreateThread(core::ptr::null_mut(), 0, watch, core::ptr::null_mut(), 0, core::ptr::null_mut());
}

unsafe fn patch_all(first: bool) {
    // index 0 = the exe; index i = MODULES[i - 1] (null while that module is not loaded: skipped)
    let mut bases = vec![GetModuleHandleW(core::ptr::null()) as *const u8];
    for m in MODULES.iter() {
        bases.push(GetModuleHandleW(m.as_ptr()) as *const u8);
    }
    for (i, base) in bases.into_iter().enumerate() {
        let system = i > 0 && is_system(&MODULES[i - 1]);
        patch_module(base, first, i, system);
    }
}

/// kernel32 / kernelbase / ucrtbase: their LoadLibrary imports are not ours to wrap (our wrappers call the
/// kernel32 LoadLibrary, which would come straight back).
fn is_system(m: &[u16]) -> bool {
    let n = String::from_utf16_lossy(&m[..m.len().saturating_sub(1)]).to_ascii_lowercase();
    matches!(n.as_str(), "kernel32.dll" | "kernelbase.dll" | "ucrtbase.dll") || n.starts_with("api-ms-")
}

unsafe fn patch_module(base: *const u8, first: bool, which: usize, system: bool) {
    if base.is_null() {
        return;
    }
    for (f, h) in [
        ("CreateFile2", h_createfile2 as *const () as usize),
        ("LoadLibraryExW", h_loadlibraryexw as *const () as usize),
        ("LoadLibraryW", h_loadlibraryw as *const () as usize),
        ("CreateFileW", h_createfilew as *const () as usize),
        ("GetFileAttributesW", h_getfileattributesw as *const () as usize),
        ("GetFileAttributesExW", h_getfileattributesexw as *const () as usize),
        ("FindFirstFileW", h_findfirstfilew as *const () as usize),
        ("FindFirstFileExW", h_findfirstfileexw as *const () as usize),
        ("FindNextFileW", h_findnextfilew as *const () as usize),
        ("FindClose", h_findclose as *const () as usize),
    ] {
        if system && f.starts_with("LoadLibrary") {
            continue;
        }
        let n = patch_iat(base, f, h);
        if first || n > 0 {
            log(&format!("patch module {which} {f}: {n}"));
        }
    }
}

unsafe fn load_real() {
    let mut sys = vec![0u16; 1024];
    let n = GetSystemDirectoryW(sys.as_mut_ptr(), 1000) as usize;
    let name = String::from_utf8_lossy(&PROXY_DLL[..PROXY_DLL.len() - 1]).to_string();
    let path = wide(&format!("{}\\{}", String::from_utf16_lossy(&sys[..n]), name));
    let m = LoadLibraryW(path.as_ptr());
    if m.is_null() {
        return;
    }
    for (i, nm) in NAMES.iter().enumerate() {
        SLOTS[i] = GetProcAddress(m, nm.as_ptr()) as usize;
    }
}

#[no_mangle]
pub unsafe extern "system" fn DllMain(_inst: Handle, reason: u32, _res: *mut c_void) -> Bool {
    if reason == 1 {
        load_real();
        activate();
    } else if reason == 0 {
        if let Some(se) = SESSION.as_ref() {
            restore(se); // the game exited normally: put the user's files back now
        }
    }
    1
}

#[cfg(test)]
mod tests {
    use super::{is_system, wide, wild};

    #[test]
    fn system_modules_skip_loadlibrary_hooks() {
        assert!(is_system(&wide("KERNEL32.DLL")));
        assert!(is_system(&wide("ucrtbase.dll")));
        assert!(!is_system(&wide("UnityPlayer.dll")));
    }

    #[test]
    fn wildcard_patterns_used_by_engine_scans() {
        assert!(wild("*.*", "zzz_tirgumim_he_p.pak"));
        assert!(wild("*", "anything"));
        assert!(wild("*.pak", "zzz_tirgumim_he_p.pak"));
        assert!(!wild("*.pak", "zzz_tirgumim_he_p.sig"));
        assert!(wild("zzz*", "zzz_tirgumim_he_p.pak"));
        assert!(wild("zzz_tirgumim_he_p.pak", "zzz_tirgumim_he_p.pak"));
        assert!(!wild("other.pak", "zzz_tirgumim_he_p.pak"));
        assert!(!wild("a*b*c", "abc")); // two stars: not supported, never matches
    }
}
