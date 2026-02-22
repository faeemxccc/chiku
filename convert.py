import os
import glob

files = glob.glob("*.py") + ["requirements.txt", ".env"]

for file in files:
    try:
        with open(file, 'rb') as f:
            content = f.read()
        try:
            text = content.decode('utf-16le')
            with open(file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Converted {file} from UTF-16LE to UTF-8")
        except UnicodeDecodeError:
            try:
                # it might be utf-8 already
                content.decode('utf-8')
                print(f"File {file} is already UTF-8")
            except:
                pass
    except Exception as e:
        print(f"Error processing {file}: {e}")
