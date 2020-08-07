import sys
from streamlit import cli as stcli

sys.argv = ["streamlit", "run", "app.py", "--global.developmentMode=false"]
sys.exit()
	
