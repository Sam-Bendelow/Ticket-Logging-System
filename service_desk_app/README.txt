# How to deploy the web app locally

1. **In VS Code open a New Terminal and run the script**
   - python -m venv venv

2. **Activate the virtual environment using**
   - venv\Scripts\Activate.ps1 (Windows)
   - venv/bin/activate (Mac

3. **Install dependencies into the virtual environment from requirements.txt**
   -  pip install -r requirements.txt

4. **Run the application locally on http://127.0.0.1:5000**
   - python run.py

5. **Optional - Reset database - The table already has data populated, however these can be regenerated with random tickets.**
   - python setup_db.py
   - python seed_db.py

# How to access the web app via AWS

1. **The app has been deployed on the web via AWS using ElasticBeanstalk**
   - Link is http://helpdeskwebapp-env.eba-pzssjn2d.eu-west-2.elasticbeanstalk.com/