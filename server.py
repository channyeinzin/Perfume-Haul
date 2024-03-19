import random
from flask import Flask, render_template, request, redirect, url_for, jsonify


app = Flask(__name__)

# Example data
items = [
    {
        "id": 1,
        "title": "Mojave Ghost",
        "image": "/static/byredo.jpg",
        "description": "Mojave Ghost by Byredo is a Amber Floral fragrance for women and men. Mojave Ghost was launched in 2014. Top notes are Sapodilla and Ambrette (Musk Mallow); middle notes are Magnolia, Violet and Sandalwood; base notes are Ambergris and Cedar.",
        "score": "8.5",
        "top_note": ["Ambrette", "Nesberry"],
        "heart_note": ["Magnolia", "Sandalwood", "Violet"],
        "base_note": ["Cedarwood", "Musks", "Vetiver"],
        "website": "https://www.byredo.com/us_en/mojaveghost-eau-de-parfum-50ml?_gl=1*1mqpwdm*_up*MQ..&gclid=CjwKCAiA6KWvBhAREiwAFPZM7iVW-GGI7SpxiFm_ym1ldbol_nrh0yeXMHXnMrpyUjzQujrZ_a4JhRoCqhAQAvD_BwE"
    },
    {
        "id": 2,
        "title": "Sauvage Dior",
        "image": "/static/dior.jpg",
        "description": "Sauvage by Dior is a Aromatic Fougere fragrance for men. Sauvage was launched in 2015. The nose behind this fragrance is François Demachy. Top notes are Calabrian bergamot and Pepper; middle notes are Sichuan Pepper, Lavender, Pink Pepper, Vetiver, Patchouli, Geranium and elemi; base notes are Ambroxan, Cedar and Labdanum.",
        "score": "8.5",
        "top_note": ["Bergamot", "Pepper"],
        "heart_note": ["Sichuan Pepper", "Lavender", "Pink Pepper", "Vetiver", "Patchouli", "Geranium", "Elemi"],
        "base_note": ["Ambroxan", "Cedar", "Labdanum"],
        "website": "https://www.dior.com/en_us/beauty/products/sauvage-eau-de-toilette-Y0685240.html"
    },
    {
        "id": 3,
        "title": "Bleu de Chanel",
        "image": "/static/chanel.jpg",
        "description": "Bleu de Chanel by Chanel is a Woody Aromatic fragrance for men. Bleu de Chanel was launched in 2010. The nose behind this fragrance is Jacques Polge. Top notes are Grapefruit, Lemon, Mint and Pink Pepper; middle notes are Ginger, Nutmeg, Jasmine and Iso E Super; base notes are Incense, Vetiver, Cedar, Sandalwood, Patchouli, Labdanum and White Musk.",
        "score": "8.5",
        "top_note": ["Bergamot", "Lemon", "Grapefruit", "Vetiver", "Pink pepper", "Marine accord"],
        "heart_note": ["Grapefruit", "Cedarwood", "Labdanum", "Peppermint", "Nutmeg", "Ginger", "Jamine"],
        "base_note": ["Frankincense", "Ginger", "New Caledonian Sandalwood", "Amber wood"],
        "website": "https://www.chanel.com/us/fragrance/p/107460/bleu-de-chanel-eau-de-toilette-spray/"
    },
]

@app.route('/')
def index():
    # Assuming you want to display all items as popular for demonstration
    popular_items = items  # This sends all items to the template
    return render_template('index.html', popular_items=popular_items)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if query:
        # This will filter the items list to only those where the query is in the title
        results = [item for item in items if query.lower() in item['title'].lower()]
    else:
        # If the query is empty or only whitespace, return no results
        results = []
    
    # The results and query are passed to the template, which will handle displaying them
    return render_template('search_results.html', results=results, query=query)



@app.route('/view/<int:item_id>')
def view_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    return render_template('view_item.html', item=item)

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    success_message = None
    error_message = None
    
    if request.method == 'POST':
        title = request.form.get('title').strip()
        description = request.form.get('description').strip()
        score = request.form.get('score').strip()
        top_note = request.form.get('top_note').strip()
        heart_note = request.form.get('heart_note').strip()
        base_note = request.form.get('base_note').strip()
        image_url = request.form.get('image_url').strip()
        website_data_link = request.form.get('website_data_link').strip()
        
        # Check if any of the fields are empty
        if not (title and description and score and top_note and heart_note and base_note and image_url and website_data_link):
            error_message = "All fields are required."
        else:
            # Splitting comma-separated fields
            top_note = top_note.split(',')
            heart_note = heart_note.split(',')
            base_note = base_note.split(',')
            
            # Determine the new item's ID
            if items:
                new_id = max(item['id'] for item in items) + 1
            else:
                new_id = 1
            
            # Add the new perfume to the items list
            new_item = {
                "id": new_id,
                "title": title,
                "description": description,
                "score": score,
                "top_note": top_note,
                "heart_note": heart_note,
                "base_note": base_note,
                "image": image_url,
                "website": website_data_link
            }
            items.append(new_item)
            
            success_message = "New item successfully created."
            
            # Check if the user wants to view the submitted item
            if request.form.get('action') == 'view':
                return redirect(url_for('view_item', item_id=new_item['id']))
    
    return render_template('add_data.html', success_message=success_message, error_message=error_message)


   
@app.route('/popular_items', methods=['GET'])
def get_popular_items():
    # Shuffle the items list randomly
    shuffled_items = random.sample(items, min(len(items), 3))
    # Return the shuffled popular items data as JSON
    return jsonify(shuffled_items)

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        item['title'] = request.form['title']
        item['description'] = request.form['description']
        item['score'] = request.form['score']
        item['top_note'] = request.form['top_note'].split(',')
        item['heart_note'] = request.form['heart_note'].split(',')
        item['base_note'] = request.form['base_note'].split(',')
        item['image'] = request.form['image_url']
        item['website'] = request.form['website_data_link']
        return redirect(url_for('view_item', item_id=item_id))

    return render_template('edit_item.html', item=item)

 


if __name__ == '__main__':
    app.run(debug=True)
