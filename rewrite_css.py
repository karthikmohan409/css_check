import re
import difflib

def extract_css_classes(css_content):
    pattern = re.compile(r'\.([a-zA-Z0-9_-]+)\s*\{([^}]*)\}')
    return pattern.findall(css_content)

def find_best_match(ai_class, ai_properties, existing_classes):
    best_match = None
    highest_ratio = 0.0
    for existing_class, existing_properties in existing_classes:
        ratio = difflib.SequenceMatcher(None, ai_properties, existing_properties).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = existing_class
    return best_match

def rewrite_css(input_css, existing_css):
    ai_classes = extract_css_classes(input_css)
    existing_classes = extract_css_classes(existing_css)
    
    framework_mapping = {}
    for ai_class, ai_properties in ai_classes:
        best_match = find_best_match(ai_class, ai_properties, existing_classes)
        if best_match:
            framework_mapping[ai_class] = best_match
    
    output_css = input_css
    for ai_class, framework_class in framework_mapping.items():
        output_css = re.sub(r'\b' + re.escape(ai_class) + r'\b', framework_class, output_css)
    
    return output_css

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    # Read AI-generated CSS
    ai_css = read_file('ai_generated.css')
    
    # Read existing CSS
    existing_css = read_file('existing.css')
    
    # Rewrite the CSS
    rewritten_css = rewrite_css(ai_css, existing_css)
    
    # Write the rewritten CSS to a new file
    write_file('rewritten_css.css', rewritten_css)
    print("Rewritten CSS has been saved to rewritten_css.css")

if __name__ == "__main__":
    main()
