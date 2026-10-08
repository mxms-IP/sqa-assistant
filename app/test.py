from rag_pipe.chunking import load_and_chunk

chunks_list=[]

chunks = load_and_chunk("data/sample/BUG-002.pdf")
chunks_list.extend(chunks)


print("---------------------------------Chunks---------------------------------")
for chunk in chunks_list:
        print(chunk)