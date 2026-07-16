def test_analyze_txt_document_returns_structured_response(
    client,
) -> None:
    response = client.post(
        "/api/v1/documents/analyze",
        files={
            "file": (
                "program.txt",
                (
                    b"Applicants must be at least 18 years old. "
                    b"Applications are due July 31. "
                    b"Government-issued identification is required."
                ),
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["document"]["filename"] == "program.txt"
    assert payload["document"]["media_type"] == "text/plain"
    assert payload["document"]["size_bytes"] > 0
    assert payload["analysis"]["executive_summary"]
    assert payload["analysis"]["eligibility_requirements"]
    assert payload["analysis"]["important_deadlines"]
    assert payload["analysis"]["required_documents"] == [
        "Government-issued identification"
    ]
    assert payload["metadata"]["provider"] == "fake"
    assert payload["metadata"]["prompt_name"] == (
        "document_operational_analysis"
    )


def test_analyze_markdown_document_returns_structured_response(
    client,
) -> None:
    response = client.post(
        "/api/v1/documents/analyze",
        files={
            "file": (
                "program.md",
                (
                    b"# Workforce Program\n\n"
                    b"Applicants must be at least 18 years old."
                ),
                "text/markdown",
            )
        },
    )

    assert response.status_code == 200
    assert response.json()["analysis"][
        "eligibility_requirements"
    ]


def test_analyze_document_rejects_unsupported_extension(
    client,
) -> None:
    response = client.post(
        "/api/v1/documents/analyze",
        files={
            "file": (
                "program.docx",
                b"Unsupported document",
                (
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == (
        "unsupported_document_type"
    )


def test_analyze_document_rejects_empty_file(
    client,
) -> None:
    response = client.post(
        "/api/v1/documents/analyze",
        files={
            "file": (
                "program.txt",
                b"",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "empty_document"


def test_analyze_document_rejects_spoofed_pdf(
    client,
) -> None:
    response = client.post(
        "/api/v1/documents/analyze",
        files={
            "file": (
                "program.pdf",
                b"This is not a PDF.",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == (
        "unsupported_document_type"
    )


def test_analyze_document_requires_file(
    client,
) -> None:
    response = client.post(
        "/api/v1/documents/analyze"
    )

    assert response.status_code == 422