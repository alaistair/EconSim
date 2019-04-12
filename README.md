# Kuznets demo
Kuznets is an economic model written in Python. It is an agent-based economic model, where individual households work and spend money at individual firms. The relationships between, say, household spending and unemployment or firm inventories and GDP growth perform as you would expect, although there is some work to do in calibrating the sensitivities to match a real economy. I'm currently working on incorporating government policy, as well as international trade and asset markets.

See a demo of the core model at [kuznets.herokuapp.com](http://kuznets.herokuapp.com). The graphs in the demo are displayed using Dash (based on Plotly). The app runs on a Flask server and is hosted on Heroku. You can run the simulation for a number of cycles and toggle various graphs. The 'Looking deeper' tab displays some interesting real-world economic relationships that the simulation can reproduce.

Eventually the goal is that someone can run the simulation, make changes to say interest rates and observe how it performs against an economy with different policy, such as following the Taylor rule.
