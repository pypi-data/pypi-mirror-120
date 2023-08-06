try:
    import finnsinte
except ModuleNotFoundError:
    pass

from sparv.api import annotator, SourceFilename


@annotator("Hej", "cool")
def apa(source_file: SourceFilename = SourceFilename()):
    finnsinte.do()
    pass
