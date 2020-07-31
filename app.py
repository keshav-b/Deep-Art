from flask import Flask, redirect, url_for, render_template, request
import os
#import style_transfer

app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'images')

app.config["IMG_UPLOADS"] = IMG_FOLDER
app.config["ALLOWED_IMG_TYPE"] = ["JPG", "jpg", "png", "PNG"]

def allowed_img(filename):
	if not "." in filename:
		return False
	else:
		ext = filename.rsplit(".",1)[1]
		if ext in app.config["ALLOWED_IMG_TYPE"]:
			return True


@app.route("/", methods=["GET", "POST"])
def predict():

	if request.method == 'POST':
		if request.files:

			content_image = request.files["content_image"] 
			style_image = request.files["style_image"] 
			
			content_image_path = os.path.join(app.config["IMG_UPLOADS"], content_image.filename)
			content_image.save(content_image_path)

			style_image_path = os.path.join(app.config["IMG_UPLOADS"], style_image.filename)
			style_image.save(style_image_path)

			c = content_image_path+content_image.filename
			s = style_image_path+style_image.filename
			
			
			style_transfer.train(content_image_path,style_image_path)
			
			target = 'static/images/target.png'
			
			
			return render_template("predict.html", content_image = content_image_path, style_image = style_image_path, target_image = target)

	return render_template("predict.html")


if __name__ == "__main__":
	app.run(debug=True)
