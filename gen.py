from flask import Flask, request, jsonify
from faker import Faker

app = Flask(__name__)


def generate_faker_data(provider_type, locale):
    fake = Faker(locale)
    if hasattr(fake, provider_type):
        return getattr(fake, provider_type)()
    return ''


def generate_insert_statement(table_name, num_records, params, locale):
    generated_data = []
    for _ in range(num_records):
        values = []
        for param in params:
            value = generate_faker_data(param['type'], locale)
            value = value.replace('\n', ' ').replace("'", "''")  # Replace line breaks and single quotes
            values.append(f"'{value}'")

        insert_statement = f"INSERT INTO {table_name} ({', '.join([param['name'] for param in params])}) VALUES ({', '.join(values)})"
        generated_data.append(insert_statement + '\n')  # Append a newline after each INSERT statement

    return ''.join(generated_data)  # Return the generated SQL statements as a single string with line breaks



@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    num_fields = int(data['numFields'])
    table_name = data['tableName']
    params = data['params']
    locale = data['locale']

    generated_data = generate_insert_statement(table_name, num_fields, params, locale)
    return generated_data


if __name__ == '__main__':
    app.run()
