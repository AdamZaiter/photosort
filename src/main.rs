extern crate fs_extra;
use fs_extra::file::*;
use fs_extra::error::*;

use std::process;
use std::fs;
use std::env;
use std::path::Path;

fn main() {
    let args: Vec<String> = env::args().collect();
    match args.len() {
        3 =>(),
        _ => {
            help();
            process::exit(0x0100); 
        }
    }
    let src_dir = &args[1];
    let dest_dir = &args[2];
    let res = copy_files(&src_dir, &dest_dir);
    match res {
        Result::Err(err) => println!("Error: {}", err),
        _=>()
    }

    println!("{}", Path::new(src_dir).exists());
}

fn help() {
    println!("Usage: [src_dir] [dest_dir]");
}
fn copy_files(src_dir: &String, dest_dir: &String) -> Result<()> {
    let paths = fs::read_dir(src_dir).unwrap();

    for (i, path) in paths.enumerate() {
        let options = CopyOptions::new();
        copy(path.unwrap().path(), format!("{}test{}.jpg", dest_dir, i), &options)?;
    }
    Ok(())
}
