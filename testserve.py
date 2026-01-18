from flask import Flask, request, send_file, redirect, url_for, render_template
import os
from urllib import parse


app = Flask(__name__)
root_folder = "/home/user/testpy/samples"  # Default folder
current_folder = "/home/user/testpy/samples"  # Default folder
previous_folder = []  # Initially no previous folder

def list_files(folder):
    files_and_folders = []
    try:
        with os.scandir(folder) as it:
            for entry in it:
                if entry.is_file():
                    file_path = os.path.join(folder, entry.name)
                    file_path = parse.quote_plus(file_path)
                    files_and_folders.append({"type": "file", "path": file_path, "name": entry.name})
                elif entry.is_dir():
                    new_folder = os.path.join(folder, entry.name)
                    new_folder = parse.quote_plus(new_folder)
                    print(f"create {new_folder}")
                    files_and_folders.append({"type": "folder", "path": new_folder, "name": entry.name})
    except Exception as e:
        print(f"Error scanning {folder}: {e}")
    return files_and_folders

@app.route('/')
def index():
    global current_folder
    current_folder = root_folder
    print(f"at root current folder:{current_folder}")
    return render_template('index.html', folder=current_folder, items=list_files(current_folder))

@app.route('/folder/<path:folder>')
def list_folder(folder):
    global current_folder, previous_folder
    new_folder = parse.unquote( folder)
    print(f"change {new_folder}")
    if os.path.isdir(new_folder):
        print(current_folder)
        print(new_folder)
        previous_folder.append(current_folder)  # Update the previous folder before changing to the new one
        current_folder = new_folder
    # return redirect(url_for('index'))
    return render_template('index.html', folder=current_folder, items=list_files(current_folder))

@app.route('/play/<path:file>')
def serve_file(file):
    file_path = parse.unquote( file)
    print(f"play file_path:{file_path}")
    if os.path.isfile(file_path):
        return send_file(file_path)
    else:
        return "File not found", 404

@app.route('/previous')
def last_folder():
    global current_folder, previous_folder
    print("SHould be going backward")
    if not previous_folder:
        return redirect(url_for('index'))
    next_folder = previous_folder.pop()
    return redirect(url_for('list_folder', folder=next_folder))

if __name__ == '__main__':
    app.run(debug=True)
