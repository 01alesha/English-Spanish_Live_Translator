# English-Spanish_Live_Translator
Project: Real-Time English–Spanish Voice Translation System

#Overview
This project implements a real-time English–Spanish voice translation pipeline, converting spoken English input into Spanish text output. The system integrates speech processing with neural machine translation, focusing on latency, output coherence, and translation quality.

#Problem Statement
Real-time translation systems require accurate transcription, robust language modeling, and efficient inference under tight latency constraints. This project explores how NLP and sequence-to-sequence models can be combined into a production-style translation pipeline.

#System Pipeline
Speech Input – English audio captured from microphone
Speech-to-Text – Audio converted into text
Neural Machine Translation – English text translated to Spanish
Output Delivery – Translated text displayed in real time

#Model & Approach
Sequence-to-sequence NMT architecture
Tokenization using custom vocabularies
Attention to sentence structure and semantic preservation
Pipeline design optimized for responsiveness

#Evaluation Focus
Translation accuracy and semantic consistency
Handling of partial or noisy inputs
Latency across pipeline stages

#Tools & Technologies
Python
TensorFlow / Keras
NLP preprocessing utilities
Audio processing libraries

#Key Learnings
Designing end-to-end NLP pipelines
Managing trade-offs between speed and translation quality
Evaluating output coherence in real-time systems

#Future Enhancements
Interactive dashboard for live monitoring
Improved handling of long or complex sentences
Model optimization for lower latency
