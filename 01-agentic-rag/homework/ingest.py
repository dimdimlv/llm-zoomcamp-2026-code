from gitsource import GithubRepositoryDataReader, chunk_documents
from minsearch import Index


REPO_OWNER = "DataTalksClub"
REPO_NAME = "llm-zoomcamp"
COMMIT_ID = "8c1834d"


def load_documents():
    reader = GithubRepositoryDataReader(
        repo_owner=REPO_OWNER,
        repo_name=REPO_NAME,
        commit_id=COMMIT_ID,
        allowed_extensions={"md"},
        filename_filter=lambda path: "/lessons/" in path,
    )
    return [f.parse() for f in reader.read()]


def build_index(documents):
    index = Index(
        text_fields=["content"],
        keyword_fields=["filename"],
    )
    index.fit(documents)
    return index


def build_chunk_index(documents, size=2000, step=1000):
    chunks = chunk_documents(documents, size=size, step=step)
    index = Index(
        text_fields=["content"],
        keyword_fields=["filename"],
    )
    index.fit(chunks)
    return chunks, index
