"""
SMART PADDY
PaddyMitra - RAG Chatbot

API-key-free chatbot backend.

This version:
- Uses the existing FAISS RAG system
- Loads index, chunks and embedding model correctly
- Restricts retrieval to the selected variety
- Keeps selected land size as context
- Does not use OpenAI API
- Does not invent agricultural information
"""

from typing import Optional

from .validator import validate_variety
from .retriever import (
    retrieve,
    format_retrieved_context,
    load_retrieval_system,
)


# ============================================================
# CHATBOT IDENTITY
# ============================================================

CHATBOT_NAME = "PaddyMitra"

CHATBOT_SUBTITLE = "Smart Paddy Cultivation Assistant"


# ============================================================
# LAND SIZE VALIDATION
# ============================================================

def validate_land_size(land_size: str) -> str:
    """
    Validate selected land size.
    """

    if land_size is None:
        raise ValueError("Land size is required.")

    value = str(land_size).strip()

    if not value:
        raise ValueError("Land size cannot be empty.")

    standard_values = {
        "1 Acre",
        "2 Acres",
        "3 Acres",
    }

    if value in standard_values:
        return value

    try:

        numeric = float(
            value
            .lower()
            .replace("acres", "")
            .replace("acre", "")
            .strip()
        )

        if numeric <= 0:
            raise ValueError

        return f"{numeric:g} Acres"

    except ValueError:

        raise ValueError(
            "Invalid land size. "
            "Use 1 Acre, 2 Acres, 3 Acres, "
            "or a positive custom value."
        )


# ============================================================
# CHAT SESSION
# ============================================================

class PaddyMitraChat:
    """
    Maintains PaddyMitra chatbot context.

    Context:
        - Selected variety
        - Land size
        - Chat history
        - RAG retrieval system
    """

    def __init__(
        self,
        selected_variety: str,
        land_size: str,
    ):

        # ----------------------------------------------------
        # Validate variety
        # ----------------------------------------------------

        self.selected_variety = validate_variety(
            selected_variety
        )

        # ----------------------------------------------------
        # Validate land
        # ----------------------------------------------------

        self.land_size = validate_land_size(
            land_size
        )

        # ----------------------------------------------------
        # Chat history
        # ----------------------------------------------------

        self.history = []

        # ----------------------------------------------------
        # Load RAG retrieval system
        # ----------------------------------------------------
        #
        # This is the important fix.
        #
        # retriever.retrieve() requires:
        #     index
        #     chunks
        #     model
        #
        # So we load them once when the chatbot starts.
        # ----------------------------------------------------

        (
            self.index,
            self.chunks,
            self.model,
        ) = load_retrieval_system()

    # ========================================================
    # CONTEXT
    # ========================================================

    def get_context(self) -> str:
        """
        Return current chatbot context.
        """

        return (
            f"Selected Paddy Variety: "
            f"{self.selected_variety}\n"
            f"Land Size: {self.land_size}"
        )

    # ========================================================
    # RETRIEVE RAG KNOWLEDGE
    # ========================================================

    def retrieve_knowledge(
        self,
        question: str,
        top_k: int = 6,
    ):
        """
        Retrieve knowledge using the existing RAG system.
        """

        if not question or not question.strip():
            return []

        results = retrieve(
            query=question,
            selected_variety=self.selected_variety,
            index=self.index,
            chunks=self.chunks,
            model=self.model,
            top_k=top_k,
        )

        return results

    # ========================================================
    # BUILD RESPONSE
    # ========================================================

    def build_response(
        self,
        question: str,
        top_k: int = 6,
    ) -> str:
        """
        Generate a grounded RAG response.

        Current version directly presents verified
        retrieved knowledge.

        Later an actual LLM can be connected here.
        """

        question = str(question).strip()

        if not question:

            return (
                f"🌾 **{CHATBOT_NAME}**\n\n"
                "Please enter your question."
            )

        # ----------------------------------------------------
        # Retrieve
        # ----------------------------------------------------

        results = self.retrieve_knowledge(
            question=question,
            top_k=top_k,
        )

        # ----------------------------------------------------
        # No results
        # ----------------------------------------------------

        if not results:

            answer = (
                f"🌾 **{CHATBOT_NAME}**\n\n"
                f"**Variety:** {self.selected_variety}\n"
                f"**Land Size:** {self.land_size}\n\n"
                "I could not find sufficient verified "
                "information in the Smart Paddy RAG "
                "knowledge base for this question.\n\n"
                "Please ask another cultivation-related "
                "question."
            )

            self.history.append(
                {
                    "user": question,
                    "assistant": answer,
                }
            )

            return answer

        # ----------------------------------------------------
        # Format RAG context
        # ----------------------------------------------------

        context = format_retrieved_context(
            results
        )

        # ----------------------------------------------------
        # Build response
        # ----------------------------------------------------

        answer_parts = [

            f"🌾 **{CHATBOT_NAME}**",

            (
                f"**Selected Variety:** "
                f"{self.selected_variety}"
            ),

            (
                f"**Land Size:** "
                f"{self.land_size}"
            ),

            "### Answer",

            (
                f"Based on the verified Smart Paddy "
                f"knowledge retrieved for "
                f"**{self.selected_variety}**:"
            ),

            context,

            "### Important",

            (
                "This response is based on verified "
                "information retrieved from the RAG "
                "knowledge base. The system does not "
                "invent unsupported fertilizer, water, "
                "seed, pesticide, labour or yield values."
            ),
        ]

        answer = "\n\n".join(answer_parts)

        # ----------------------------------------------------
        # Save history
        # ----------------------------------------------------

        self.history.append(
            {
                "user": question,
                "assistant": answer,
            }
        )

        return answer

    # ========================================================
    # HISTORY
    # ========================================================

    def get_history(self):

        return self.history

    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    def clear_history(self):

        self.history = []


# ============================================================
# STREAMLIT HELPER
# ============================================================

def ask_paddymitra(
    question: str,
    selected_variety: str,
    land_size: str,
    top_k: int = 6,
) -> str:
    """
    Simple helper for Streamlit.
    """

    chatbot = PaddyMitraChat(
        selected_variety=selected_variety,
        land_size=land_size,
    )

    return chatbot.build_response(
        question=question,
        top_k=top_k,
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("🌾 PADDYMITRA - RAG CHATBOT TEST")
    print("=" * 70)

    try:

        # ----------------------------------------------------
        # Create chatbot
        # ----------------------------------------------------

        chatbot = PaddyMitraChat(
            selected_variety="Sannalu",
            land_size="2 Acres",
        )

        print(
            "\nChatbot Name:",
            CHATBOT_NAME
        )

        print(
            "Selected Variety:",
            chatbot.selected_variety
        )

        print(
            "Land Size:",
            chatbot.land_size
        )

        print(
            "\nRAG index loaded:",
            chatbot.index is not None
        )

        print(
            "RAG chunks loaded:",
            len(chatbot.chunks)
        )

        print(
            "Embedding model loaded:",
            chatbot.model is not None
        )

        # ----------------------------------------------------
        # Test questions
        # ----------------------------------------------------

        test_questions = [
            "What is Sannalu rice?",
            "What should I know about water management?",
        ]

        for question in test_questions:

            print("\n" + "-" * 70)

            print("QUESTION:")
            print(question)

            print("\nSearching RAG...")

            answer = chatbot.build_response(
                question=question,
                top_k=6,
            )

            print("\nANSWER:")
            print(answer[:6000])

        print("\n" + "=" * 70)
        print(
            "SUCCESS: PaddyMitra RAG chatbot test completed."
        )
        print("=" * 70)

    except Exception as e:

        print("\n" + "=" * 70)
        print("CHATBOT TEST FAILED")
        print("=" * 70)

        print(
            type(e).__name__ + ":",
            e
        )