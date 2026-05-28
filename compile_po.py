# compile_po.py
import os
import sys

import polib

# List of languages you want to compile
LANGUAGES = ['uz', 'ru']

print("🚀 Starting .po deduplication and compilation...")

for lang in LANGUAGES:
    po_path = f'locale/{lang}/LC_MESSAGES/django.po'
    mo_path = f'locale/{lang}/LC_MESSAGES/django.mo'

    if not os.path.exists(po_path):
        print(f"⚠️  Skipped {lang}: {po_path} not found.")
        continue

    try:
        # Read the .po file
        po = polib.pofile(po_path)
        initial_count = len(po)
        
        # Deduplicate: Later items naturally overwrite earlier ones in a dict
        unique_entries = {}
        for entry in po:
            # Grouping by both context (msgctxt) and message ID (msgid) 
            # prevents accidentally breaking valid gettext contextual variations
            key = (entry.msgctxt, entry.msgid)
            unique_entries[key] = entry

        # Clear the original list and fill it with the unique, latest entries
        del po[:]
        for entry in unique_entries.values():
            po.append(entry)

        # Log optimization metrics and sync the source file if changes occurred
        duplicates_removed = initial_count - len(po)
        if duplicates_removed > 0:
            po.save(po_path)
            print(f"🧹 Cleaned {lang}: Removed {duplicates_removed} older duplicate entries from source.")

        # Compile and save as .mo file
        po.save_as_mofile(mo_path)
        print(f"✅ Compiled {lang} successfully!")
        
    except Exception as e:
        print(f"❌ Error processing {lang}: {e}")

print("\n🎉 Done! Clean translation catalogs compiled.")