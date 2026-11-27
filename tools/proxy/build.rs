// Generates the export stubs for the DLL named by PROXY_DLL (default xinput1_3) from exports/<name>.txt.
// Each line: `Name @ordinal` (ordinal optional). Every export is a `jmp [slot]` into the real System32 DLL.
use std::{env, fs, path::PathBuf};
fn main() {
    let dll = env::var("PROXY_DLL").unwrap_or_else(|_| "xinput1_3".into());
    println!("cargo:rerun-if-env-changed=PROXY_DLL");
    println!("cargo:rerun-if-changed=exports/{dll}.txt");
    let list = fs::read_to_string(format!("exports/{dll}.txt")).expect("exports list");
    let out = PathBuf::from(env::var("OUT_DIR").unwrap());
    let mut def = format!("LIBRARY {dll}\nEXPORTS\n");
    let mut asm = String::from(".text\n");
    let mut names = String::new();
    let mut n = 0;
    for line in list.lines().map(str::trim).filter(|l| !l.is_empty() && !l.starts_with('#')) {
        let mut it = line.split_whitespace();
        let name = it.next().unwrap();
        let ord = it.next().map(|o| o.trim_start_matches('@').to_string());
        def += &format!("  {name}=tg_stub_{n}{}\n", ord.map(|o| format!(" @{o}")).unwrap_or_default());
        asm += &format!(".globl tg_stub_{n}\ntg_stub_{n}:\n  jmp qword ptr [rip + {{slots}} + {}]\n", n * 8);
        names += &format!("b\"{name}\0\",");
        n += 1;
    }
    fs::write(out.join("exports.def"), def).unwrap();
    fs::write(
        out.join("stubs.rs"),
        format!(
            "pub const PROXY_DLL: &[u8] = b\"{dll}.dll\0\";\npub const NAMES: [&[u8]; {n}] = [{names}];\n#[no_mangle] pub static mut SLOTS: [usize; {n}] = [0; {n}];\ncore::arch::global_asm!(r#\"{asm}\"#, slots = sym SLOTS);\n"
        ),
    )
    .unwrap();
    println!("cargo:rustc-cdylib-link-arg=/DEF:{}", out.join("exports.def").display());
}
