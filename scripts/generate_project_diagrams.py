from __future__ import annotations

import textwrap
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover - artifact helper
    raise SystemExit(
        "Pillow is required to generate the project diagrams. "
        "Use the bundled runtime or install Pillow locally."
    ) from exc


OUTPUT_DIR = Path("docs/diagrams")
WIDTH = 1800
HEIGHT = 1200


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def draw_gradient_background(image: Image.Image, start: tuple[int, int, int], end: tuple[int, int, int]) -> None:
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        ratio = y / (HEIGHT - 1)
        color = tuple(
            int(start[idx] * (1 - ratio) + end[idx] * ratio)
            for idx in range(3)
        )
        draw.line([(0, y), (WIDTH, y)], fill=color)


def draw_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    title_font: ImageFont.ImageFont,
    text_font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
) -> None:
    draw.rounded_rectangle(box, radius=26, fill=fill)
    x1, y1, x2, y2 = box
    draw.text((x1 + 28, y1 + 24), title, font=title_font, fill=(15, 23, 42))
    cursor_y = y1 + 82
    max_width = x2 - x1 - 56
    for line in lines:
        wrapped = textwrap.wrap(line, width=30)
        for subline in wrapped:
            draw.text((x1 + 28, cursor_y), subline, font=text_font, fill=(30, 41, 59))
            cursor_y += 28
        cursor_y += 6


def draw_bullets(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    lines: list[str],
    text_font: ImageFont.ImageFont,
) -> None:
    x1, y1, _, _ = box
    cursor_y = y1 + 100
    for line in lines:
        draw.ellipse((x1 + 30, cursor_y + 9, x1 + 44, cursor_y + 23), fill=(29, 78, 216))
        draw.text((x1 + 60, cursor_y), line, font=text_font, fill=(30, 41, 59))
        cursor_y += 42


def build_diagram(
    output_path: Path,
    background_start: tuple[int, int, int],
    background_end: tuple[int, int, int],
    accent: tuple[int, int, int],
    subtitle_color: tuple[int, int, int],
    title: str,
    subtitle: str,
    cards: list[tuple[tuple[int, int, int, int], str, list[str]]],
    pipeline_title: str,
    pipeline_line: str,
    pipeline_note_1: str,
    pipeline_note_2: str,
    left_title: str,
    left_bullets: list[str],
    right_title: str,
    right_bullets: list[str],
) -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), color=background_start)
    draw_gradient_background(image, background_start, background_end)
    draw = ImageDraw.Draw(image)

    title_font = load_font(56, bold=True)
    subtitle_font = load_font(28)
    card_title_font = load_font(34, bold=True)
    card_text_font = load_font(22)
    section_title_font = load_font(34, bold=True)
    body_font = load_font(28)
    pipeline_font = load_font(30, bold=True)

    draw.text((90, 78), title, font=title_font, fill=(255, 255, 255))
    draw.text((90, 142), subtitle, font=subtitle_font, fill=subtitle_color)

    card_fill = (245, 249, 255)
    for box, card_title, card_lines in cards:
        draw_card(
            draw,
            box,
            card_title,
            card_lines,
            card_title_font,
            card_text_font,
            card_fill,
        )

    pipeline_box = (90, 590, 1710, 810)
    draw.rounded_rectangle(pipeline_box, radius=26, fill=(245, 249, 255))
    draw.text((125, 588), pipeline_title, font=section_title_font, fill=(15, 23, 42))
    draw.text((125, 654), pipeline_line, font=pipeline_font, fill=accent)
    draw.text((125, 714), pipeline_note_1, font=card_text_font, fill=(30, 41, 59))
    draw.text((125, 754), pipeline_note_2, font=card_text_font, fill=(30, 41, 59))

    left_box = (90, 850, 780, 1110)
    right_box = (930, 850, 1710, 1110)
    draw.rounded_rectangle(left_box, radius=26, fill=(245, 249, 255))
    draw.rounded_rectangle(right_box, radius=26, fill=(245, 249, 255))
    draw.text((125, 868), left_title, font=section_title_font, fill=(15, 23, 42))
    draw.text((965, 868), right_title, font=section_title_font, fill=(15, 23, 42))
    draw_bullets(draw, left_box, left_bullets, body_font)
    draw_bullets(draw, right_box, right_bullets, body_font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="JPEG", quality=95)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    build_diagram(
        output_path=OUTPUT_DIR / "project-overview-ru.jpg",
        background_start=(15, 23, 42),
        background_end=(29, 78, 216),
        accent=(29, 78, 216),
        subtitle_color=(219, 234, 254),
        title="Enterprise AI Operations Assistant",
        subtitle="Архитектура проекта, flow данных, ключевой стек и сильные стороны решения",
        cards=[
            (
                (90, 220, 640, 570),
                "1. Входы в систему",
                [
                    "REST API: upload / search / ask / agent / workflows",
                    "MCP server: tools, resource, prompt template",
                    "n8n webhooks: automation и orchestration",
                    "Future clients: Telegram, CRM",
                    "and external APIs",
                ],
            ),
            (
                (675, 220, 1175, 570),
                "2. Логика backend",
                [
                    "FastAPI routes",
                    "Services: extraction, chunking, retrieval, rag",
                    "Agents: router, knowledge_agent, action_agent",
                    "Actions + workflow dispatcher",
                ],
            ),
            (
                (1210, 220, 1710, 570),
                "3. Инфраструктура",
                [
                    "PostgreSQL: metadata и document chunks",
                    "Qdrant: vector search",
                    "Redis: infra-ready cache / queue layer",
                    "Docker Compose + n8n",
                ],
            ),
        ],
        pipeline_title="Как работает основной pipeline",
        pipeline_line="upload → store → extract text → chunk → index in Qdrant → semantic search → RAG answer",
        pipeline_note_1="Agent layer выбирает маршрут: search / ask / action",
        pipeline_note_2="Workflow layer через n8n автоматизирует process / chunk / index и notification flows",
        left_title="Ключевой стек",
        left_bullets=[
            "Python • FastAPI • SQLAlchemy • PostgreSQL",
            "Qdrant • OpenAI API • LangChain • MCP",
            "n8n • Docker Compose • RAG • AI Agents",
        ],
        right_title="Что делает проект сильным",
        right_bullets=[
            "Полный document pipeline",
            "Grounded RAG по документам",
            "MCP-ready и workflow-ready архитектура",
        ],
    )

    build_diagram(
        output_path=OUTPUT_DIR / "project-overview-en.jpg",
        background_start=(17, 24, 39),
        background_end=(15, 118, 110),
        accent=(15, 118, 110),
        subtitle_color=(204, 251, 241),
        title="Enterprise AI Operations Assistant",
        subtitle="Project architecture, data flow, core stack, and key solution strengths",
        cards=[
            (
                (90, 220, 640, 570),
                "1. System entry points",
                [
                    "REST API: upload / search / ask / agent / workflows",
                    "MCP server: tools, resource, prompt template",
                    "n8n webhooks for workflow orchestration",
                    "Future clients: Telegram, CRM",
                    "and external APIs",
                ],
            ),
            (
                (675, 220, 1175, 570),
                "2. Backend logic",
                [
                    "FastAPI routes",
                    "Services: extraction, chunking, retrieval, rag",
                    "Agents: router, knowledge_agent, action_agent",
                    "Actions + workflow dispatcher",
                ],
            ),
            (
                (1210, 220, 1710, 570),
                "3. Infrastructure",
                [
                    "PostgreSQL for metadata and chunks",
                    "Qdrant for vector search",
                    "Redis as infra-ready cache / queue layer",
                    "Docker Compose + n8n",
                ],
            ),
        ],
        pipeline_title="Main pipeline",
        pipeline_line="upload → store → extract text → chunk → index in Qdrant → semantic search → RAG answer",
        pipeline_note_1="The agent layer selects the route: search / ask / action",
        pipeline_note_2="The workflow layer uses n8n to automate process / chunk / index and notification flows",
        left_title="Core stack",
        left_bullets=[
            "Python • FastAPI • SQLAlchemy • PostgreSQL",
            "Qdrant • OpenAI API • LangChain • MCP",
            "n8n • Docker Compose • RAG • AI Agents",
        ],
        right_title="What makes it strong",
        right_bullets=[
            "Full document processing pipeline",
            "Grounded RAG over real documents",
            "MCP-ready and workflow-ready architecture",
        ],
    )

    print("Generated docs/diagrams/project-overview-ru.jpg")
    print("Generated docs/diagrams/project-overview-en.jpg")


if __name__ == "__main__":
    main()
