import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf(filename="cloud_ai_pricing_report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36, leftMargin=36,
        topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1A365D") # Navy
    secondary_color = colors.HexColor("#2B6CB0") # Blue
    dark_neutral = colors.HexColor("#2D3748")
    light_bg = colors.HexColor("#F7FAFC")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=dark_neutral,
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=dark_neutral,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=dark_neutral
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell_style,
        alignment=1
    )

    story = []

    story.append(Paragraph("Comprehensive Multi-Cloud AI Provider & API Pricing Report (2025â2026)", title_style))
    story.append(Paragraph("Exhaustive Analysis of OpenAI, Anthropic, DeepSeek, Google Gemini, GroqCloud, Cloudflare Workers AI, OpenCode, OpenRouter & Together AI + Best Personal API Strategy", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceAfter=8))

    story.append(Paragraph("1. Executive Summary & Market Overview", h1_style))
    story.append(Paragraph(
        "The AI cloud inference market has expanded rapidly into an ultra-competitive ecosystem. Beyond traditional frontier labs (OpenAI, Anthropic, Google), developers and power-users now have access to specialized high-speed hosting (GroqCloud, Cloudflare Workers AI), open-weight aggregators (OpenRouter, Together AI), disruptive low-cost architectures (DeepSeek), and specialized coding agent networks (OpenCode). This report details every major provider's token pricing, free tiers, and identifies the absolute best API configuration for personal usage and development.",
        body_style
    ))

    story.append(Paragraph("2. Comprehensive Provider & Model Pricing Matrix (Per 1 Million Tokens)", h1_style))
    story.append(Paragraph(
        "The table below synthesizes current pricing across all major cloud model providers, highlighting input/output costs, context windows, and free tiers.",
        body_style
    ))

    table_data = [
        [
            Paragraph("Provider / Ecosystem", table_header_style),
            Paragraph("Representative Models", table_header_style),
            Paragraph("Input ($ / 1M)", table_header_style),
            Paragraph("Output ($ / 1M)", table_header_style),
            Paragraph("Context Window", table_header_style),
            Paragraph("Free Tier / Key Notes", table_header_style)
        ],
        [
            Paragraph("<b>Google AI Studio</b>", table_cell_style),
            Paragraph("Gemini Flash / Pro", table_cell_style),
            Paragraph("Free / $0.075", table_cell_center),
            Paragraph("Free / $0.30", table_cell_center),
            Paragraph("1M - 2M tokens", table_cell_center),
            Paragraph("<b>Generous Free Tier</b>. Elite long-context capability in AI Studio.", table_cell_style)
        ],
        [
            Paragraph("<b>DeepSeek</b>", table_cell_style),
            Paragraph("DeepSeek-V4-Flash / Pro", table_cell_style),
            Paragraph("$0.15", table_cell_center),
            Paragraph("$0.60", table_cell_center),
            Paragraph("64k - 128k", table_cell_center),
            Paragraph("Disruptive low pricing. Off-peak discounts & cached input savings.", table_cell_style)
        ],
        [
            Paragraph("<b>GroqCloud</b>", table_cell_style),
            Paragraph("GPT-OSS 120B / 20B", table_cell_style),
            Paragraph("$0.15 / $0.075", table_cell_center),
            Paragraph("$0.60 / $0.30", table_cell_center),
            Paragraph("32k - 128k", table_cell_center),
            Paragraph("<b>Blazing Fast</b> (~500 tokens/sec via LPUs). 50% batch discounts.", table_cell_style)
        ],
        [
            Paragraph("<b>Cloudflare Workers AI</b>", table_cell_style),
            Paragraph("Granite / Llama / GLM", table_cell_style),
            Paragraph("$0.017 - $1.40", table_cell_center),
            Paragraph("$0.112 - $4.40", table_cell_center),
            Paragraph("8k - 128k", table_cell_center),
            Paragraph("10,000 Neurons/day free. Billed via Neurons ($0.011 / 1k).", table_cell_style)
        ],
        [
            Paragraph("<b>OpenCode</b>", table_cell_style),
            Paragraph("Console / Go Plans", table_cell_style),
            Paragraph("Varies by tier", table_cell_center),
            Paragraph("Varies by tier", table_cell_center),
            Paragraph("Aggregated", table_cell_center),
            Paragraph("$10/mo Go plan or Console pay-as-you-go for coding agents.", table_cell_style)
        ],
        [
            Paragraph("<b>OpenRouter</b>", table_cell_style),
            Paragraph("Multi-Model Aggregator", table_cell_center),
            Paragraph("Maker pricing", table_cell_center),
            Paragraph("Maker pricing", table_cell_center),
            Paragraph("Aggregated", table_cell_center),
            Paragraph("<b>25+ Free Models</b> available. Single unified API key.", table_cell_style)
        ],
        [
            Paragraph("<b>OpenAI API</b>", table_cell_style),
            Paragraph("GPT-4.1 / GPT-4.1 mini", table_cell_style),
            Paragraph("$2.00 / $0.40", table_cell_center),
            Paragraph("$8.00 / $1.60", table_cell_center),
            Paragraph("128k - 1M", table_cell_center),
            Paragraph("Standard pay-as-you-go. Cached input 75% discount.", table_cell_style)
        ],
        [
            Paragraph("<b>Anthropic Claude</b>", table_cell_style),
            Paragraph("Claude 3.7 Sonnet / Haiku", table_cell_style),
            Paragraph("$3.00 / $0.80", table_cell_center),
            Paragraph("$15.00 / $4.00", table_cell_center),
            Paragraph("200k tokens", table_cell_center),
            Paragraph("Industry benchmark for complex reasoning, coding & analysis.", table_cell_style)
        ],
        [
            Paragraph("<b>Together AI</b>", table_cell_style),
            Paragraph("GLM-5.3 / Serverless", table_cell_style),
            Paragraph("$1.32 - $1.40", table_cell_center),
            Paragraph("$3.96 - $4.40", table_cell_center),
            Paragraph("128k tokens", table_cell_center),
            Paragraph("Serverless open-weights & dedicated B200 GPU clusters.", table_cell_style)
        ]
    ]

    t = Table(table_data, colWidths=[90, 105, 75, 75, 70, 125])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Detailed Provider Profiles & Nuances", h1_style))
    
    story.append(Paragraph("Google AI Studio (Gemini API)", h2_style))
    story.append(Paragraph(
        "Google provides an exceptional developer entry point with a <b>generous free tier</b> on Gemini Flash models. Its standout feature is the massive 1M to 2M token context window, allowing entire codebases, financial repositories, or multi-hundred-page PDFs to be processed in a single prompt.",
        body_style
    ))

    story.append(Paragraph("DeepSeek API", h2_style))
    story.append(Paragraph(
        "DeepSeek disrupted the market with ultra-low pricing ($0.15/M input, $0.60/M output for Flash). It offers near-frontier performance at a fraction of US commercial lab costs, making it ideal for heavy programmatic usage.",
        body_style
    ))

    story.append(Paragraph("GroqCloud", h2_style))
    story.append(Paragraph(
        "Groq utilizes proprietary LPUs to deliver blistering speeds (~500 tokens/sec). With models like GPT-OSS 120B ($0.15/M input) and 50% batch/caching discounts, it provides unmatched real-time responsiveness.",
        body_style
    ))

    story.append(Paragraph("Cloudflare Workers AI", h2_style))
    story.append(Paragraph(
        "Cloudflare integrates AI inference directly into edge workers. It includes 10,000 Neurons/day free, billing usage via Neurons ($0.011 / 1,000 Neurons) mapped to underlying model GPU compute costs.",
        body_style
    ))

    story.append(Paragraph("OpenCode & OpenRouter", h2_style))
    story.append(Paragraph(
        "<b>OpenCode</b> specializes in coding agents, offering monthly subscription plans (e.g., $10/mo Go plan) and console inference. <b>OpenRouter</b> acts as the ultimate multi-model aggregator, hosting <b>25+ free models</b> and routing across 54+ companies through a single OpenAI-compatible API key.",
        body_style
    ))

    story.append(Paragraph("OpenAI, Anthropic & Together AI", h2_style))
    story.append(Paragraph(
        "<b>OpenAI</b> (GPT-4.1) and <b>Anthropic</b> (Claude 3.7 Sonnet) remain the gold standards for elite coding, complex reasoning, and nuance. <b>Together AI</b> bridges open-weight serverless execution with dedicated GPU clusters.",
        body_style
    ))

    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Best Plan & Strategy for Personal Usage", h1_style))
    story.append(Paragraph(
        "For personal developers, hobbyists, and power-users seeking maximum value without high overhead, the recommended multi-provider strategy is:",
        body_style
    ))

    story.append(Paragraph("<b>1. Primary Free Tier & Long Context: Google AI Studio (Gemini)</b>", bullet_style))
    story.append(Paragraph(
        "â¢ <i>Why:</i> Free access within generous developer limits + 1M-2M context windows makes it unbeatable for research and prototyping.",
        bullet_style
    ))

    story.append(Paragraph("<b>2. Ultra-Low Cost Production & Coding: DeepSeek API</b>", bullet_style))
    story.append(Paragraph(
        "â¢ <i>Why:</i> Pay-as-you-go at $0.15/$0.60 per 1M tokens provides elite intelligence for programmatic scripts and assistants at minimal cost.",
        bullet_style
    ))

    story.append(Paragraph("<b>3. Sandbox & Free Testing: OpenRouter</b>", bullet_style))
    story.append(Paragraph(
        "â¢ <i>Why:</i> Gives instant access to 25+ free models and unified switching across all major upstream labs.",
        bullet_style
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Conclusion:</b> Start entirely free with <b>Google AI Studio</b> for massive documents, and fund a small $10 prepaid balance on <b>DeepSeek API</b> for lightning-fast programmatic tasks.", body_style))

    doc.build(story)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    generate_pdf()
