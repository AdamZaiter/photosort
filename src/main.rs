extern crate fs_extra;
use fs_extra::error::Result;
use fs_extra::file::copy;
use fs_extra::file::CopyOptions;

extern crate rexif;

use std::env;
use std::fs;
use std::io;
use std::io::prelude::Write;
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

fn copy_files(src_dir: &str, dest_dir: &str) -> Result<()> {
    let paths_count = match fs::read_dir(src_dir) {
        Ok(res) => res,
        Err(err) => panic!("Error procesing args: {:?}", err),
    };
    let paths_count = paths_count;
    let mut num_of_files: u32 = 0;
    let mut copied_files: u32 = 0;
    for file in paths_count {
        let temp_fpath = file.unwrap().path();
        let temp_fname = format!("{}", temp_fpath.display());
        if temp_fname.ends_with(".jpg") {
            num_of_files += 1;
        }
    }
    let paths = fs::read_dir(src_dir).unwrap();
    for path in paths {
        print!("\rProgress: {}/{} files", copied_files, num_of_files);
        io::stdout().flush().ok().expect("Could not flush stdout");

        let options = CopyOptions::new();
        let file_path = path.unwrap().path();
        let file_name = format!("{}", file_path.display());
        if file_name.ends_with(".jpg") {
            let mut found_exif = 0;
            match rexif::parse_file(&file_name) {
                Ok(exif) => {
                    for entry in &exif.entries {
                        match entry.tag {
                            rexif::ExifTag::DateTime => {
                                let new_fname = format_exif_file_name(entry, dest_dir);
                                found_exif = 1;
                                copy(&file_path, new_fname, &options)?;
                            }
                            _ => (),
                        }
                    }
                    if found_exif == 0 {
                        let new_fname = format_unknown_file_name(dest_dir);
                        copy(&file_path, new_fname, &options)?;
                    }
                }
                _ => {
                    let new_fname = format_unknown_file_name(dest_dir);
                    copy(&file_path, new_fname, &options)?;
                }
            }
            copied_files += 1;
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
fn format_exif_file_name(entry: &rexif::ExifEntry, dest_dir: &str) -> String {
    let date = entry.value.to_string();
    let date_split: Vec<_> = date.split(" ").collect();
    let ymd: Vec<_> = date_split[0].split(":").collect();
    let formatted_date = format!("{}-{}-{}", ymd[0], ymd[2], ymd[1]);
    let year = ymd[0];
    let mut new_fname = format!("{}photos/{}/{}.jpg", dest_dir, ymd[0], formatted_date);
    std::fs::create_dir_all(format!("{}/photos/{}", dest_dir, year))
        .expect("Directory couldn't be created");
    let mut ctr = 1;
    while Path::new(&new_fname).exists() {
        new_fname = format!(
            "{}photos/{}/{}({}).jpg",
            dest_dir,
            year,
            formatted_date,
            num_to_str_fmt(ctr)
        );
        ctr += 1;
    }
    new_fname
}
fn format_unknown_file_name(dest_dir: &str) -> String {
    let mut ctr = 1;
    let mut new_fname = format!("{}photos/unknown/{}.jpg", dest_dir, ctr);
    std::fs::create_dir_all(format!("{}photos/unknown/", dest_dir))
        .expect("Directory couldn't be created");
    while Path::new(&new_fname).exists() {
        new_fname = format!("{}photos/unknown/{}.jpg", dest_dir, num_to_str_fmt(ctr));
        ctr += 1;
    }
    new_fname
}

fn num_to_str_fmt(num: i32) -> String {
    match num.to_string().len() {
        1 => format!("{}{}", "00", num),
        2 => format!("{}{}", "0", num),
        _ => num.to_string(),
    }
}
