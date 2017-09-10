from providers import model_provider

model = model_provider.load()

print('classifier ready')


@app.route('/classify')
def classify():
    print('classify')
