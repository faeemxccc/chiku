from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flash_messages'  # Replace with a real secret key if needed

CONTEXT_FILE = 'chat_context.json'

def load_context():
    if not os.path.exists(CONTEXT_FILE):
        return {}
    try:
        with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_context(data):
    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    context_data = load_context()
    return render_template('index.html', context_data=context_data)

@app.route('/export/<user_id>')
def export_user(user_id):
    context_data = load_context()
    if user_id in context_data:
        from flask import Response
        import json
        
        data = json.dumps(context_data[user_id], indent=4, ensure_ascii=False)
        return Response(
            data,
            mimetype="application/json",
            headers={"Content-disposition": f"attachment; filename=user_{user_id}_memories.json"}
        )
    flash('User not found for export.', 'error')
    return redirect(url_for('index'))

@app.route('/edit/<user_id>/<int:index>', methods=['POST'])
def edit_memory(user_id, index):
    context_data = load_context()
    
    if user_id in context_data and 0 <= index < len(context_data[user_id]):
        new_role = request.form.get('role')
        new_text = request.form.get('text')
        
        if new_role and new_text:
            context_data[user_id][index]["role"] = new_role
            context_data[user_id][index]["text"] = new_text
            save_context(context_data)
            flash('Memory updated successfully!', 'success')
        else:
            flash('Both role and text are required.', 'error')
    else:
        flash('Invalid memory reference.', 'error')
        
    return redirect(url_for('index'))

@app.route('/delete/<user_id>/<int:index>', methods=['POST'])
def delete_memory(user_id, index):
    context_data = load_context()
    
    if user_id in context_data and 0 <= index < len(context_data[user_id]):
        deleted_item = context_data[user_id].pop(index)
        
        # If the user's memories are now empty, remove the user key
        if not context_data[user_id]:
            del context_data[user_id]
            
        save_context(context_data)
        flash('Memory deleted successfully!', 'success')
    else:
        flash('Invalid memory reference.', 'error')
        
    return redirect(url_for('index'))

@app.route('/clear/<user_id>', methods=['POST'])
def clear_user(user_id):
    context_data = load_context()
    
    if user_id in context_data:
        del context_data[user_id]
        save_context(context_data)
        flash(f'All memories for user {user_id} have been cleared.', 'success')
    else:
        flash('User not found.', 'error')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
