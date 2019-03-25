# Kuznets
Kuznets is an interactive economics tutor. It is a web-based economics course that forgoes the standard MOOC filmed lecture/multiple choice template, and instead allows a student to interact with an economic model, which can explain concepts to students in a more targeted way and build intuition faster. The goal is for it to teach a novice the key concepts in Greg Mankiw's undergraduate Macroeconomics textbook in three hours or less.

The core of Kuznets is an economic simulation where individual households and firms cooperate, along with government, financial markets, and international economies.

Different concepts can be revealed as the student progresses. In the early stages it is made clear that economic growth is the result of people creating things that other people want. In later stages they can change monetary policy and see the effect on inflation, economic activity, and asset prices. Tax policy changes will affect hiring decisions and working decisions, as well as the distribution of income.

Data generated from the simulation can be used to illustrate various relationships. Okun's law can be seen by plotting unemployment and GDP growth. The effects of interest rate changes can be plotted on an IS-LM curve. Kuznets handles all the data work so that the charts can be drawn at will (or when the student is at an appropriate level), which speeds up the intuition.

I am currently implementing the simulation in Python and will have a minimum viable version of the model soon. The next stage will be developing a front-end (likely in React given that the data are visualised in Dash) and then a back end to handle the users and data. Following that will be developing the content and testing the results.

# Why Kuznets

Australia is seeing a precipitous decline in the study of economics. Enrolment in Yr 12 Economics has fallen by 70 per cent over the past 25 years, with even steeper declines seen in the enrolment of females and of public school students. Declining interest in economics has been observed in other countries, including the United States and United Kingdom (with the steepest declines seen among those not white, relatively wealthy, or male, although there have been declines within that cohort too).

In Australia the Reserve Bank has lobbied the state government to adjust the high school curriculum in favour of economics.

Economist Tyler Cowen, in his book Stubborn Attachments, makes the case that the

I have tinkered with various toy economic models in the past, and in high school I created a circular flow of income in Visual Basic to explain how the economy works.

When looking at the options currently available for online economics teaching it is striking that

The initial market to address is CFA students. Surveys show each student spends at least 300 hours on each of the Level I and Level II exams. Meanwhile the pass rate for the June 2017 Level II was 47%.

enrolments

# Kuznets.co

The platform is named in honour of Simon Kuznets, an economist who, among other things, helped create the concept of Gross National Product, devised measures to compute it, won a Nobel Prize for his work on economic growth and how countries at similar stages of development are nonetheless different, and discovered a relationship between income inequality and economic growth.

# About me

I graduated from The University of Western Australia with degrees in Economics (Hons) and Computer Science. While at UWA I tutored Macroeconomics 101 and Monetary Economics 210. I am a Senior Analyst at the Reserve Bank of Australia.
