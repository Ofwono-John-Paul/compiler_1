from compiler_pipeline import DEFAULT_SOURCE, compile_source


def main() -> None:
    result = compile_source(DEFAULT_SOURCE)

    if not result["success"]:
        print(f"Compilation failed at {result['stage']}: {result['error']}")
        return

    print("TOKENS")
    for token in result["tokens"]:
        print(
            f"{token['type']}:{token['value']} "
            f"(Line {token['line']}, Col {token['column']})"
        )

    print("\nAST (PARSE TREE)")
    print(result["parse_tree"])

    print("\nSEMANTIC CHECK")
    print("Passed")

    print("\nOPTIMIZED AST")
    print(result["optimized_ast"])

    print("\nGENERATED CODE")
    print(result["generated_code"])

    print("\nEXECUTION OUTPUT")
    print(result["execution_output"], end="")


if __name__ == "__main__":
    main()