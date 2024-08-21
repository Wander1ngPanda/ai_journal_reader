# AI Journal Reader
This is a Python app that is able to read through scientific journals and be able to answer questions regarding the content and findings

Goal Learn about AI, Embeddings and How Langchain works

It should also be able to run offline using llama but might also add chatgpt and open ai ability

I intend to have it working within a streamlit application

Stages:

1. Have the program run from a CLI and interact with a preloaded directory with 1 Article
    (This is focusing on the AI portion of the app. Can I set it up so that I can get useful information out of it at the end. More importantly, can I understand what each aspect of the code is doing)
2. Add additional articles and have it handle answering questions regarding each of them
    is it able to identify which article the information is out of. Its useful to have it cite sources
    (This is probably more prompt engineering. Having the program give structured responses and limit how it can interact or respond. Put Tight parameters and controls to keep it within scope)
3. Can I have this run through a Streamlit application
    (This is playing around with UI design. Making something that is intuitive to interact with)
4. Instead of providing with an article could I have it point at a website and have it download an article if it is freely avaliable


Note: I wonder if Llava is able to analyse graphs


Note, Next project idea. Use a Kaggle dataset and a postgres database. Enable natural language sql queries. How can this be tested. How can it be broken.




Current Stage:
- I have a basic app that allows me to make one query at a time

Next Goal
- CUrrently breaks if a file isnt loaded
- Add code to either lock the typing field or hide the field until a file is loaded
- Enable multiple queries without re embedding the dataset
    - Computationally expensive, Llama3 can interact fast locally but is slow to embed. Wouldnt be a problem to embed first and then use an llm with the new vecor stuff

