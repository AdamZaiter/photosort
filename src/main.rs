extern crate fs_extra;
use fs_extra::error::*;
use fs_extra::file::*;

extern crate rexif;

use std::env;
use std::fs;
use std::io;
use std::io::prelude::*;
use std::path::Path;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    match args.len() {
        3 => (),
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
        _ => (),
    }
}

fn help() {
    println!("Usage: [src_dir] [dest_dir]");
}
fn copy_files(src_dir: &String, dest_dir: &String) -> Result<()> {
    let paths_count = fs::read_dir(src_dir).unwrap();
    let mut num_of_files: u32 = 0;
    let mut copied_files: u32 = 0;
    for file in paths_count {
        let f_p = file.unwrap().path();
        let f_n = format!("{}", f_p.display());
        if f_n.ends_with(".jpg") {
            num_of_files += 1;
        }
    }
    let paths = fs::read_dir(src_dir).unwrap();
    for path in paths {
        print!("\rProgress: {}/{} files", copied_files, num_of_files);
        io::stdout().flush().ok().expect("Could not flush stdout");
        // std::thread::sleep(std::time::Duration::from_secs(1));
        let options = CopyOptions::new();
        let file_path = path.unwrap().path();
        let file_name = format!("{}", file_path.display());
        if file_name.ends_with(".jpg") {
            match rexif::parse_file(&file_name) {
                Ok(exif) => {
                    for entry in &exif.entries {
                        match entry.tag {
                            rexif::ExifTag::DateTime => {
                                let date = entry.value.to_string();
                                let date_split: Vec<_> = date.split(" ").collect();
                                let formatted_date = date_split[0].replace(":", "_");
                                let mut new_fname = format!("{}{}.jpg", dest_dir, formatted_date);
                                let mut ctr = 1;
                                while Path::new(&new_fname).exists() {
                                    new_fname =
                                        format!("{}{}({}).jpg", dest_dir, formatted_date, ctr);
                                    ctr += 1;
                                }
                                copy(&file_path, new_fname, &options)?;
                                copied_files += 1;
                            }
                            _ => (),
                        }
                    }
                }
                Err(_e) => print!("xxx"),
            }
        }
    }
    print!("\rProgress: {}/{} files", copied_files, num_of_files);
    if num_of_files - copied_files != 0 {
        println!(
            "\n{} files could not be copied.",
            num_of_files - copied_files
        );
    }
    Ok(())
}
