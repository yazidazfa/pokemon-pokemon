import requests
from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)
db_name = 'pokemon.db'
connection = sqlite3.connect(db_name,check_same_thread=False)



table_pokemon_creation_query = """
    CREATE TABLE IF NOT EXISTS POKEMON
    (
        id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        base_experience INTEGER NOT NULL,
        weight INTEGER NOT NULL,
        image_path VARCHAR(255) NOT NULL
    );
"""

table_abilities_creation_query = """
    CREATE TABLE IF NOT EXISTS ABILITIES
    (
        id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
"""

table_pokemon_abilities_creation_query = """
    CREATE TABLE IF NOT EXISTS POKEMON_ABILITIES
    (
        pokemon_id INTEGER PRIMARY KEY,
        abilities_id INTEGER NOT NULL,
        FOREIGN KEY (pokemon_id) REFERENCES POKEMON(id),
        FOREIGN KEY (abilities_id) REFERENCES ABILITIES(id)
    );
"""



@app.route('/get_pokemon', methods=['GET'])
def get_pokemon():
    connection = sqlite3.connect(db_name,check_same_thread=False)
    cursor = connection.cursor()
    for i in range(1, 401):
        request_pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}')
        if request_pokemon.status_code == 200:
            data = request_pokemon.json()
            name = data['name']
            base_experience = data['base_experience']
            weight = data['weight']
            image_path = f'asset/{i}.png'

            if weight >= 100:
                cursor.execute("INSERT INTO POKEMON (id, name, base_experience, weight, image_path) VALUES (?, ?, ?, ?, ?)",
                           (i, name, base_experience, weight, image_path))

            else:
                print(f"Pokemon with id {i} weight less than 100 not inserted.")
        else:
            print(f"Failed to retrieve data for Pokemon ID {i}")

    
    connection.commit()

    return {"message": "Pokemon fetched successfully"}

asset_folder = os.path.join(app.root_path, 'asset')
app.config['UPLOAD_FOLDER'] = asset_folder

@app.route('/', methods=['GET'])
def index():
    connection = sqlite3.connect(db_name,check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(table_pokemon_creation_query)
    cursor.execute(table_abilities_creation_query)
    cursor.execute(table_pokemon_abilities_creation_query)

    cursor.execute("SELECT * FROM POKEMON")
    pokemons = cursor.fetchall()
    pokemons = [
        {
            "id": p[0],
            "name": p[1],
            "base_experience": p[2],
            "weight": p[3],
            "image_path": p[4]
        } for p in pokemons
    ]
    connection.close()

    # return {"pokemons": pokemons}
    return render_template('index.html', pokemons=pokemons)

if __name__ == '__main__':
    app.run(debug=True)