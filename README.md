# Kuznets
Kuznets is my idea for an interactive economics tutor with a realistically specified economic model that students can play with to learn hands on, instead of just watching video lectures like in a MOOC. Individual households and firms cooperate to build wealth in the model, with government, financial markets, and international economies playing a part.

As the student progresses, different economic concepts can be revealed. In the early stages it is made clear that economic growth is the result of people creating things that other people want. In later stages they can change monetary policy and see the effect on inflation, economic activity, and asset prices, and observe the effects of the changes versus, say, following the Taylor rule. Tax policy changes will affect hiring decisions and working decisions, as well as the distribution of income.

Kuznets will also use the data generated from the simulation to illustrate various relationships. Okun's law can be seen by plotting unemployment and GDP growth. The effects of interest rate changes can be plotted on an IS-LM curve. Kuznets handles all the data work so that the charts can be drawn at will (or when the student is at an appropriate level), which speeds up the intuition.

# Kuznets.co demo
Kuznets so far consists of a core economic model, which is written in Python. It is an agent-based economic simulation, where individual households work and spend money at individual firms. The relationships between, say, household spending and unemployment or firm inventories and GDP growth perform as you would expect, although there is some work to do in calibrating the sensitivities to match a real economy. Eventually it will incorporate government policy, as well as international trade and asset markets.

The graphs in the demo are displayed using Dash (based on Plotly). The app runs on a Flask server and is hosted on Heroku. See a demo of the core model at [kuznets.herokuapp.com](http://kuznets.herokuapp.com).

The platform is named in honour of Simon Kuznets, an economist who, among other things, helped create the concept of Gross National Product, devised measures to compute it, won a Nobel Prize for his work on economic growth and how countries at similar stages of development are nonetheless different, and discovered a relationship between income inequality and economic growth.

# Why Kuznets

Australia is seeing a [precipitous decline](https://www.rba.gov.au/speeches/2018/sp-so-2018-05-26.html) in the study of economics. Enrolment in Yr 12 Economics has fallen by 70 per cent over the past 25 years, with even steeper declines seen in the enrolment of females and of public school students. Declining interest in economics has been observed in other countries, including the United States and United Kingdom.

Economist Tyler Cowen, in his book Stubborn Attachments, makes a strong case for the pursuit of 'wealth plus', broadly defined as GDP as well as leisure, household production, and environmental amenities. Public policy, and individual decisions, should be made in light of maximising wealth plus, Cowen argues, taking into account human rights and morality.

These are all great points but the declining interest in economics among young people suggests that they are falling on deaf ears. One possible reason is that economics as a subject is perceived as dry, 'mathy', and subject to bias. My hope is that Kuznets can alleviate some of these misconceptions.

I personally think it would be great if our grandchildren look back in sadness at our time of relative poverty, and see how resource constraints meant that for example many of our own grandparents suffered for decades because we did not have the resources to pay for Alzheimers research. The way to make this happen of course is to ensure that our grandchildren inherit a much wealthier economy.

# About me

I graduated from The University of Western Australia with degrees in Economics (Hons) and Computer Science. While at UWA I tutored Macroeconomics 101 and Monetary Economics 210. As an economist I helped build macroeconomic models for stress testing banks' portfolios.
