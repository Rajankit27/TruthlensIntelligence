path = r'a:\cursor review2_experiment\TruthLens-AI\backend\app.py'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

marker = 'return render_template("index.html")'
idx = content.find(marker)
if idx == -1:
    print("Marker not found!")
else:
    insert_after = idx + len(marker)
    snippet = (
        '\r\n\r\n\r\n@app.route("/footer-demo")\r\n'
        'def footer_demo():\r\n'
        '    """Serve the footer demo page."""\r\n'
        '    return render_template("footer_demo.html")'
    )
    # Check if already added
    if '/footer-demo' in content:
        print("Route already present.")
    else:
        content = content[:insert_after] + snippet + content[insert_after:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("SUCCESS: /footer-demo route added.")
