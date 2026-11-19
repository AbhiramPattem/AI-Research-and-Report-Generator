
from .crew import run_pipeline


def run():

    topic = input(
        "\nEnter your research topic: "
    )

    try:

        result = run_pipeline(topic)

        print("\n========== FINAL RESEARCH REPORT ==========\n")

        print(result)

        with open(
            "research_report.md",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(str(result))

        print(
            "\nReport saved as research_report.md"
        )

    except Exception as e:

        print("\nPipeline execution failed!")
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    run()
