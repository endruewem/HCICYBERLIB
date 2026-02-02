import os
import json

# --- KONFIGURASI PATH ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
COURSE_DIR = os.path.join(ROOT_DIR, 'data', 'course')
OUTPUT_FILE = os.path.join(ROOT_DIR, 'data', 'course_data.js')

VIDEO_EXT = ('.mp4', '.mkv', '.webm')
DOC_EXT = ('.ppt', '.pptx', '.pdf')

def scan_courses():
    print("="*40)
    print("   DIAGNOSTIC MODE: GENERATE COURSE")
    print("="*40)
    print(f"[INFO] Script berjalan di: {ROOT_DIR}")
    print(f"[INFO] Mencari folder course di: {COURSE_DIR}")

    if not os.path.exists(COURSE_DIR):
        print(f"\n[FATAL ERROR] Folder 'data/course' TIDAK DITEMUKAN!")
        print(f"Path yang dicari: {COURSE_DIR}")
        print("Pastikan nama folder 'data' dan 'course' huruf kecil semua.")
        return

    courses = []
    
    # Cek isi folder course
    items_in_course = os.listdir(COURSE_DIR)
    print(f"[INFO] Isi folder 'course': {items_in_course}")

    # Level 1: Kategori
    category_folders = sorted([f for f in items_in_course if os.path.isdir(os.path.join(COURSE_DIR, f))])
    
    if not category_folders:
        print("[WARNING] Tidak ada folder Kategori (Level 1) ditemukan.")

    for cat_name in category_folders:
        print(f"\n[SCAN] Memeriksa Kategori: '{cat_name}'")
        cat_path = os.path.join(COURSE_DIR, cat_name)
        
        course_obj = {
            "title": cat_name,
            "folderName": cat_name,
            "chapters": []
        }

        # Level 2: Chapter
        chapter_folders = sorted([f for f in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, f))])
        
        if not chapter_folders:
            print(f"   -> [KOSONG] Tidak ada folder Chapter di dalam '{cat_name}'. File video tidak boleh ditaruh langsung disini!")

        for chap_name in chapter_folders:
            print(f"   -> [SCAN] Memeriksa Chapter: '{chap_name}'")
            chap_path = os.path.join(cat_path, chap_name)
            
            chapter_obj = {
                "title": chap_name,
                "folderName": chap_name,
                "files": []
            }

            # Level 3: File
            all_files = sorted(os.listdir(chap_path))
            
            for f in all_files:
                file_path = os.path.join(chap_path, f)
                if not os.path.isfile(file_path) or f.startswith('.'): continue

                ext = os.path.splitext(f)[1].lower()
                
                if ext in VIDEO_EXT:
                    print(f"      + [VIDEO] Ditemukan: {f}")
                    chapter_obj["files"].append({
                        "type": "video",
                        "name": os.path.splitext(f)[0].replace("_", " "),
                        "file": f,
                        "sub": "" # Disederhanakan untuk diagnosa
                    })
                elif ext in DOC_EXT:
                    print(f"      + [DOC]   Ditemukan: {f}")
                    chapter_obj["files"].append({
                        "type": "doc",
                        "docType": ext.replace('.', '').upper(),
                        "name": os.path.splitext(f)[0].replace("_", " "),
                        "file": f
                    })
                else:
                    print(f"      - [SKIP]  File diabaikan (ekstensi salah): {f}")

            if not chapter_obj["files"]:
                print(f"      ! [WARNING] Chapter '{chap_name}' kosong atau tidak ada file mp4/pdf.")
            
            if chapter_obj["files"]:
                course_obj["chapters"].append(chapter_obj)

        if course_obj["chapters"]:
            courses.append(course_obj)
        else:
            print(f"   ! [SKIP] Kategori '{cat_name}' diabaikan karena tidak ada konten valid.")

    # Simpan
    print("\n" + "-"*40)
    if courses:
        js_content = f"const courses = {json.dumps(courses, indent=4)};"
        try:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(js_content)
            print(f"[SUKSES] Berhasil menulis {len(courses)} course ke:")
            print(f"{OUTPUT_FILE}")
        except Exception as e:
            print(f"[ERROR] Gagal menulis file: {e}")
    else:
        print("[GAGAL] Tidak ada data course yang berhasil diproses.")
        print("Mohon cek struktur folder Anda.")

if __name__ == "__main__":
    scan_courses()
    input("\nTekan Enter untuk keluar...")