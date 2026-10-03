import os
import pandas as pd
from tqdm.auto import tqdm
from typesafe_sdk import Choice, TypeSafeClient

os.environ["TYPESAFE_API_KEY"] = (
    "apikey_2937d98637891ce4575b7ec6a35ffe753f0_aecc47490b9e9b252e05bd1b815fa75cdb8b1030e0c9ceae322d395b37c0b0da"
)

def jev_sentiment_classifier(
    df: pd.DataFrame,
    coluna_texto: str = "review",
    coluna_target: str = "sentiment",
    model: str = "jev-latest",
) -> pd.DataFrame:
    """
    Classifica reviews do IMDB utilizando Jev/TypeSafe.

    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame contendo as reviews.

    coluna_texto : str
        Coluna contendo o texto da review.

    coluna_target : str
        Coluna contendo o sentimento real.

    model : str
        Modelo Jev utilizado.

    Retorno
    -------
    pd.DataFrame
        DataFrame original acrescido das colunas:

        jev_sentiment
        jev_confidence
        jev_correct
        jev_error
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df precisa ser um pandas.DataFrame.")

    if coluna_texto not in df.columns:
        raise ValueError(
            f"Coluna '{coluna_texto}' não encontrada. "
            f"Colunas disponíveis: {df.columns.tolist()}"
        )

    if coluna_target not in df.columns:
        raise ValueError(
            f"Coluna '{coluna_target}' não encontrada. "
            f"Colunas disponíveis: {df.columns.tolist()}"
        )

    if not os.getenv("TYPESAFE_API_KEY"):
        raise EnvironmentError(
            "A variável de ambiente TYPESAFE_API_KEY " "não está configurada."
        )

    result = df.copy()

    result["jev_sentiment"] = None
    result["jev_confidence"] = None
    result["jev_correct"] = None
    result["jev_error"] = None

    with TypeSafeClient() as client:

        for idx in tqdm(
            result.index, total=len(result), desc="Classificando reviews"
        ):

            review = result.loc[idx, coluna_texto]

            if pd.isna(review) or not str(review).strip():

                result.loc[idx, "jev_sentiment"] = None

                result.loc[idx, "jev_error"] = "Review vazia"

                continue

            review = str(review)

            try:

                response = client.system_one(
                    state=review,
                    questions={
                        "sentiment": Choice(
                            instructions="""
                            Classify the sentiment of the movie
                            review.

                            Determine whether the reviewer expresses
                            an overall positive or negative opinion
                            about the movie.

                            Focus on the overall sentiment expressed
                            by the reviewer, rather than isolated
                            positive or negative words.
                            """,
                            criteria={
                                "positive": """
                                The review expresses an overall
                                positive opinion about the movie.
                                The reviewer generally liked,
                                enjoyed, praised, recommended or
                                appreciated the movie.
                                """,
                                "negative": """
                                The review expresses an overall
                                negative opinion about the movie.
                                The reviewer generally disliked,
                                criticized, regretted watching or
                                did not recommend the movie.
                                """,
                            },
                        )
                    },
                    model=model,
                )

                sentiment = response.answers["sentiment"]

                prediction = sentiment.choice

                result.loc[idx, "jev_sentiment"] = prediction

                if hasattr(sentiment, "confidence"):

                    result.loc[idx, "jev_confidence"] = sentiment.confidence

                real = str(result.loc[idx, coluna_target]).lower().strip()

                result.loc[idx, "jev_correct"] = prediction.lower() == real

            except Exception as e:

                result.loc[idx, "jev_error"] = str(e)

    return result
