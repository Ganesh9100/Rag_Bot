import re
from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TextChunker:
    def __init__(self):
        self.model = None

    # Function to split text into sentences
    def _split_sentences(self, text):
        return re.split(r'(?<=[.?!])\s+', text)

    # Function to combine adjacent sentences with a buffer
    def _combine_sentences(self, sentences, buffer_size=1):
        # Iterate through each sentence and combine with nearby sentences based on buffer size
        for i in range(len(sentences)):
            combined_sentence = ''
            for j in range(i - buffer_size, i):
                if j >= 0:
                    combined_sentence += str(sentences[j]['sentence']) + ' '
            combined_sentence += str(sentences[i]['sentence'])
            for j in range(i + 1, i + 1 + buffer_size):
                if j < len(sentences):
                    combined_sentence += ' ' + str(sentences[j]['sentence'])
            sentences[i]['combined_sentence'] = combined_sentence
        return sentences

    # Function to calculate cosine distances between combined sentences
    def _calculate_cosine_distances(self, sentences):
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]['combined_sentence_embedding']
            embedding_next = sentences[i + 1]['combined_sentence_embedding']
            # Calculate cosine similarity
            similarity = cosine_similarity([embedding_current], [embedding_next])[0][0]
            # Convert to cosine distance
            distance = 1 - similarity
            # Append cosine distance to the list
            distances.append(distance)
            # Store distance in the dictionary
            sentences[i]['distance_to_next'] = distance
        return distances, sentences

    # Main function to chunk text into meaningful parts
    def chunk_text(self, text):
        # Split text into individual sentences
        single_sentences_list = self._split_sentences(text)
        # Combine adjacent sentences
        sentences = self._combine_sentences(single_sentences_list)
        
        # Embed sentences using Hugging Face embeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        embeddings = embeddings.embed_documents([x['combined_sentence'] for x in sentences])
        
        # Associate embeddings with sentences
        for i, sentence in enumerate(sentences):
            sentence['combined_sentence_embedding'] = embeddings[i]
        
        # Calculate cosine distances between combined sentences
        distances, sentences = self._calculate_cosine_distances(sentences)
        
        # Determine breakpoints for chunking
        breakpoint_percentile_threshold = 65
        breakpoint_distance_threshold = np.percentile(distances, breakpoint_percentile_threshold)
        indices_above_thresh = [i for i, x in enumerate(distances) if x > breakpoint_distance_threshold]

        # Create chunks based on breakpoints
        start_index = 0
        chunks = []
        for index in indices_above_thresh:
            end_index = index
            group = sentences[start_index:end_index + 1]
            combined_text = ' '.join([str(d['sentence']) for d in group])
            chunks.append(combined_text)
            start_index = index + 1
        
        # Handle the last group, if any sentences remain
        if start_index < len(sentences):
            combined_text = ' '.join([str(d['sentence']) for d in sentences[start_index:]])
            chunks.append(combined_text)
        
        return chunks



text = "insert your text here"

chunker = TextChunker()
chunks = chunker.chunk_text(text)




def _split_sentences(self, text):
text_sentences = re.split(r'(?<=[.?!])\s+', text)
return [{"sentence": sentence} for sentence in text_sentences]
