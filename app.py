from flask import Flask, render_template, jsonify, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

app.secret_key = "caircocoders-ednalan"

DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "51654372985"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def main():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM carbrands ORDER BY brand_id")
    carbrands = cur.fetchall()
    return render_template('index.html', carbrands=carbrands)


@app.route("/carbrand", methods=["POST"])
def carbrand():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    brand_id = request.form.get('brand_id')

    if brand_id:
        cur.execute("SELECT * FROM carmodels WHERE brand_id = %s ORDER BY car_model ASC", [brand_id])
        cars = cur.fetchall()
        car_characteristics = []

        for car in cars:
            car_characteristics.append({
                'model_id': car['model_id'],
                'car_model': car['car_model'],
            })

        return jsonify(car_characteristics)

    return jsonify([])


@app.route("/carcharacteristics", methods=["POST"])
def carcharacteristics():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    brand_id = request.form.get('brand_id')
    model_id = request.form.get('model_id')

    if brand_id and model_id:
        cur.execute("SELECT * FROM carmodels WHERE brand_id = %s AND model_id = %s", [brand_id, model_id])
        car = cur.fetchone()

        if car:
            car_characteristics = {
                'car_photo': car['car_photo'],
                'brand_name': car['brand_name'],
                'model_id': car['model_id'],
                'car_model': car['car_model'],
                'price_range': car['price_range'],
                'year': car['year'],
                'mileage': car['mileage'],
                'transmission': car['transmission'],
                'fuel_type': car['fuel_type'],
                'color': car['color'],
                'technical_condition': car['technical_condition'],
                'customs_cleared': car['customs_cleared'],
                'driven_from': car['driven_from'],
                'engine_name': car['engine_name'],
                'location': car['location'],
                'seller_id': car['seller_id']
            }

            return jsonify(car_characteristics)

    return jsonify({})


@app.route("/filter", methods=["POST"])
def filter_cars():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    brand_id = request.form.get('brand_id')
    model_id = request.form.get('model_id')
    transmission = request.form.get('transmission')
    min_price = request.form.get('min_price')
    max_price = request.form.get('max_price')
    min_year = request.form.get('min_year')
    max_year = request.form.get('max_year')
    min_mileage = request.form.get('min_mileage')  
    max_mileage = request.form.get('max_mileage')
    engine_name = request.form.get('engine_name')   
    location = request.form.get('location')
    

    query = "SELECT * FROM carmodels WHERE 1=1"

    params = []
    if brand_id:
        query += " AND brand_id = %s"
        params.append(brand_id)
    if model_id:
        query += " AND model_id = %s"
        params.append(model_id)
    if transmission:
        query += " AND transmission = %s"
        params.append(transmission)
    if min_price:
        query += " AND price_range >= %s"
        params.append(min_price)
    if max_price:
        query += " AND price_range <= %s"
        params.append(max_price)
    if min_year:
        query += " AND year >= %s"
        params.append(min_year)
    if max_year:
        query += " AND year <= %s"
        params.append(max_year)
    if min_mileage:
        query += " AND mileage >= %s"
        params.append(min_mileage)
    if max_mileage:
        query += " AND mileage <= %s"
        params.append(max_mileage)
    if engine_name:
        query += " AND engine_name = %s"
        params.append(engine_name)
    if location:
        query += " AND location = %s"
        params.append(location)  

    query += " ORDER BY car_model ASC"

    cur.execute(query, params)
    cars = cur.fetchall()

    filtered_cars = []
    for car in cars:
        filtered_cars.append({
                'car_photo': car['car_photo'],
                
                'model_id': car['model_id'],
                'car_model': car['car_model'],
                'price_range': car['price_range'],
                'year': car['year'],
                'mileage': car['mileage'],
                'transmission': car['transmission'],
                'fuel_type': car['fuel_type'],
                'color': car['color'],
                'technical_condition': car['technical_condition'],
                'customs_cleared': car['customs_cleared'],
                'driven_from': car['driven_from'],
                'engine_name': car['engine_name'],
                'location': car['location'],
                'seller_id': car['seller_id']
        })

    return jsonify(filtered_cars)


if __name__ == "__main__":
    app.run(debug=True)
