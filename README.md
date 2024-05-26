# LaCarte

## Inspiration

In today's world, the ability to read quickly and learn efficiently is more crucial than ever. (Hello Arxiv readers) 

With LaCarte, we introduce a new paradigm transforming text into interactive Q&A flashcards. This not only accelerates reading/learning but also makes it more effective and enjoyable.

## What it does

LaCarte takes any blob of text and converts it into a series of question-and-answer flashcards. This process leverages MistralAI Api and LLM-as-a-judge to ensure the generated content is relevant, accurate, and non_redundant.

## How we built it

API Integration, we use the **Mistral API** to streamline the creation of Q&A pairs: 
- Initial Call: The first call determines the number of questions needed based on the text length and complexity.
- Q&A Generation: The second call generates the specific Q&A pairs.

Evaluation Pipeline: 
We developed evaluation pipelines on W&B to iteratively test and refine the prompting and the parameters to influence the quality of the generated flashcards.

Frontend:
Flask routes and JS

Hosting:
AWS

## Challenges We Ran Into:

**Quality Evaluation**: Assessing the quality and relevance of automatically generated Q&A pairs was a significant challenge. We had to develop robust evaluation metrics and feedback loops to ensure the flashcards meet high standards of educational value. How to define representativity, truthness, and redundancy ? We finally used a reference Q&A dataset SQuAD and mesures quality with LLM-as-a-Judge powered by MistralAI.

## Accomplishments that we're proud of

**Functionality and Reliability**: LaCarte is fully functional, hosted, and ready for users. It has undergone thorough evaluation and is prepared for iterative improvement based on user feedback.

**User-Centric Design**: We’ve focused on creating a clean and intuitive user interface that enhances the overall learning experience.

## What we learned

What We Learned: Iterative Metric Based Development: Continuous improvement based on rmetric feedback is essential especially with LLM. We learned the importance of iterating quickly and efficiently to refine our product thanks to W&B tool.


## What's next for LaCarte

Expanding Use Cases: 
- We plan to extend LaCarte's capabilities to include chunking PDF documents into Q&A pairs, allowing for even more versatile applications in different learning contexts.

Generalization: 
- We think converting Chunks of text into Q&A pair could be useful for creating a knowledge ready for RAG application or for many other applications. 


## Installation
```bash
git clone ...
pip install -r requirements.txt
```


## Start the webapp

```bash
python app/application.py
```


## Evaluation run

It runs an evaluation of the model on W&B with MistralAI API LLM-AS-A-Judge

Please download the dataset from https://rajpurkar.github.io/SQuAD-explorer/ and place it the evaluation folder

```bash
python app/evaluation/wand_eval.py
```