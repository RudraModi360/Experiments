import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(filename="cloud_ai_pricing_presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_slide_layout = prs.slide_layouts[6]
    
    NAVY = RGBColor(26, 54, 93)
    BLUE = RGBColor(43, 108, 176)
    DARK = RGBColor(45, 55, 72)
    LIGHT_BG = RGBColor(247, 250, 252)
    WHITE = RGBColor(255, 255, 255)
    TEAL = RGBColor(49, 151, 149)

    def add_header(slide, title_text, subtitle_text):
        header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        header.fill.solid()
        header.fill.fore_color.rgb = NAVY
        header.line.color.rgb = NAVY
        
        tf = header.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.6)
        tf.margin_top = Inches(0.15)
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = 'Helvetica'
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = 'Helvetica'
        p2.font.size = Pt(13)
        p2.font.color.rgb = RGBColor(203, 213, 225)

    def style_table_cell(cell, text, bold=False, color=DARK, bg_color=None, font_size=11, align=PP_ALIGN.LEFT):
        cell.text = text
        if bg_color:
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
        p = cell.text_frame.paragraphs[0]
        p.alignment = align
        p.font.name = 'Helvetica'
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.color.rgb = color

    # SLIDE 1
    slide = prs.slides.add_slide(blank_slide_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = NAVY
    bg.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "AI Cloud Providers & API Pricing Report"
    p.font.name = 'Helvetica'
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(15)

    p2 = tf.add_paragraph()
    p2.text = "Comprehensive Model Comparison, Pricing Matrix, & Best Personal API Strategy (2025â2026)"
    p2.font.name = 'Helvetica'
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(30)

    p3 = tf.add_paragraph()
    p3.text = "Covering OpenAI, Anthropic, DeepSeek, Google Gemini, GroqCloud, Cloudflare, OpenCode, OpenRouter & Together AI"
    p3.font.name = 'Helvetica'
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEAL

    # SLIDE 2
    slide = prs.slides.add_slide(blank_slide_layout)
    add_header(slide, "1. Executive Summary & Market Ecosystem", "The AI inference market has matured into an ultra-competitive multi-cloud landscape")

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True

    points = [
        ("Extreme Price Compression:", " Fierce competition among frontier labs and open-weight hosters has driven token prices down dramatically throughout 2025 and 2026."),
        ("Diverse Specialized Infrastructures:", " Developers now choose between ultra-low cost providers (DeepSeek), blazing-speed LPU hosting (GroqCloud), edge AI (Cloudflare Workers AI), and coding-agent aggregators (OpenCode)."),
        ("Generous Free Tiers & Sandboxes:", " Platforms like Google AI Studio (free Gemini tier) and OpenRouter (25+ free models) enable robust zero-cost personal prototyping."),
        ("Strategic Personal Takeaway:", " A hybrid setup leveraging Google AI Studio for long-context tasks and DeepSeek API for low-cost programmatic scripts offers the absolute best ROI for personal usage.")
    ]

    for title, desc in points:
        p = tf.add_paragraph()
        p.space_after = Pt(14)
        run1 = p.add_run()
        run1.text = title
        run1.font.name = 'Helvetica'
        run1.font.bold = True
        run1.font.size = Pt(16)
        run1.font.color.rgb = NAVY
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = 'Helvetica'
        run2.font.size = Pt(15)
        run2.font.color.rgb = DARK

    # SLIDE 3
    slide = prs.slides.add_slide(blank_slide_layout)
    add_header(slide, "2. Comprehensive Pricing Matrix (Part 1: Frontier & Low-Cost)", "Per 1 Million Tokens Pricing across Major Providers")

    rows, cols = 5, 6
    left, top, width, height = Inches(0.6), Inches(1.4), Inches(12.133), Inches(5.2)
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.3)
    table.columns[2].width = Inches(1.4)
    table.columns[3].width = Inches(1.4)
    table.columns[4].width = Inches(1.8)
    table.columns[5].width = Inches(3.033)

    headers = ["Provider", "Representative Models", "Input ($/1M)", "Output ($/1M)", "Context Window", "Free Tier / Key Notes"]
    for i, h in enumerate(headers):
        style_table_cell(table.cell(0, i), h, bold=True, color=WHITE, bg_color=NAVY, font_size=12, align=PP_ALIGN.CENTER)

    data_p1 = [
        ["Google AI Studio", "Gemini Flash / Pro", "Free / $0.075", "Free / $0.30", "1M - 2M tokens", "Generous Free Tier in AI Studio; massive 2M context."],
        ["DeepSeek API", "DeepSeek-V4-Flash / Pro", "$0.15", "$0.60", "64k - 128k", "Disruptive low pricing. Off-peak discounts & cached input savings."],
        ["GroqCloud", "GPT-OSS 120B / 20B", "$0.15 / $0.075", "$0.60 / $0.30", "32k - 128k", "Blazing Fast (~500 tokens/sec via LPUs). 50% batch discounts."],
        ["Cloudflare Workers AI", "Granite / Llama / GLM", "$0.017 - $1.40", "$0.112 - $4.40", "8k - 128k", "10,000 Neurons/day free. Billed via Neurons ($0.011 / 1k)."]
    ]

    for row_idx, row_data in enumerate(data_p1, start=1):
        bg = LIGHT_BG if row_idx % 2 == 1 else WHITE
        for col_idx, val in enumerate(row_data):
            align = PP_ALIGN.CENTER if col_idx in [2, 3, 4] else PP_ALIGN.LEFT
            style_table_cell(table.cell(row_idx, col_idx), val, bold=(col_idx==0), color=DARK, bg_color=bg, font_size=11, align=align)

    # SLIDE 4
    slide = prs.slides.add_slide(blank_slide_layout)
    add_header(slide, "2. Comprehensive Pricing Matrix (Part 2: Aggregators & Labs)", "Per 1 Million Tokens Pricing across Aggregators & Commercial Labs")

    rows, cols = 6, 6
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.3)
    table.columns[2].width = Inches(1.4)
    table.columns[3].width = Inches(1.4)
    table.columns[4].width = Inches(1.8)
    table.columns[5].width = Inches(3.033)

    for i, h in enumerate(headers):
        style_table_cell(table.cell(0, i), h, bold=True, color=WHITE, bg_color=NAVY, font_size=12, align=PP_ALIGN.CENTER)

    data_p2 = [
        ["OpenCode", "Console / Go Plans", "Varies by tier", "Varies by tier", "Aggregated", "$10/mo Go plan or Console pay-as-you-go for coding agents."],
        ["OpenRouter", "Multi-Model Aggregator", "Maker pricing", "Maker pricing", "Aggregated", "25+ Free Models available. Single unified API key."],
        ["OpenAI API", "GPT-4.1 / GPT-4.1 mini", "$2.00 / $0.40", "$8.00 / $1.60", "128k - 1M", "Standard pay-as-you-go. Cached input 75% discount."],
        ["Anthropic Claude", "Claude 3.7 Sonnet / Haiku", "$3.00 / $0.80", "$15.00 / $4.00", "200k tokens", "Industry benchmark for complex reasoning, coding & analysis."],
        ["Together AI", "GLM-5.3 / Serverless", "$1.32 - $1.40", "$3.96 - $4.40", "128k tokens", "Serverless open-weights & dedicated B200 GPU clusters."]
    ]

    for row_idx, row_data in enumerate(data_p2, start=1):
        bg = LIGHT_BG if row_idx % 2 == 1 else WHITE
        for col_idx, val in enumerate(row_data):
            align = PP_ALIGN.CENTER if col_idx in [2, 3, 4] else PP_ALIGN.LEFT
            style_table_cell(table.cell(row_idx, col_idx), val, bold=(col_idx==0), color=DARK, bg_color=bg, font_size=11, align=align)

    # SLIDE 5
    slide = prs.slides.add_slide(blank_slide_layout)
    add_header(slide, "3. Detailed Provider Profiles (Google, DeepSeek, Groq)", "Analysis of performance, context limits, and cost structure")

    box_width, box_height = Inches(3.8), Inches(5.3)
    boxes = [
        ("Google AI Studio", "â¢ Generous free tier for developers.\nâ¢ Massive 1M to 2M token context windows.\nâ¢ Ideal for processing entire codebases or multi-hundred-page documents in a single prompt.", Inches(0.6)),
        (
            "DeepSeek API",
            "â¢ Disruptive low pricing ($0.15/M input, $0.60/M output for Flash).\nâ¢ Near-frontier performance at a fraction of US commercial lab costs.\nâ¢ Unbeatable for high-volume programmatic tasks.",
            Inches(4.766)
        ),
        (
            "GroqCloud",
            "â¢ Proprietary LPUs deliver blistering speeds (~500 tokens/sec).\nâ¢ Models like GPT-OSS 120B ($0.15/M input).\nâ¢ 50% batch & prompt-caching discounts for extreme real-time responsiveness.",
            Inches(8.933)
        )
    ]

    for title, desc, left_pos in boxes:
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.5), box_width, box_height)
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = RGBColor(203, 213, 225)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Helvetica'
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = NAVY
        p.space_after = Pt(12)
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = 'Helvetica'
        p2.font.size = Pt(13)
        p2.font.color.rgb = DARK

    # SLIDE 6
    slide = prs.slides.add_slide(blank_slide_layout)
    add_header(slide, "3. Detailed Provider Profiles (Cloudflare, OpenCode, OpenRouter)", "Edge inference, coding agent subscriptions, and aggregators")

    boxes_p2 = [
        ("Cloudflare Workers AI", "â¢ Edge inference integrated directly into Cloudflare Workers.\nâ¢ Includes 10,000 Neurons/day free.\nâ¢ Billed via Neurons ($0.011 / 1k) mapped to underlying model GPU compute costs.", Inches(0.6)),
        (
            "OpenCode",
            "â¢ Tailored monthly subscription plans ($10/mo Go plan) and console inference.\nâ¢ Specialized for coding agents and open models.\nâ¢ Serving popular open-weight and proprietary coding models seamlessly.",
            Inches(4.766)
        ),
        (
            "OpenRouter",
            "â¢ Ultimate multi-model aggregator with unified OpenAI-compatible API.\nâ¢ Hosts 25+ free models and 4 free upstream providers.\nâ¢ Perfect sandbox for testing models without adding credit card details.",
            Inches(8.933)
        )
    ]

    for title, desc, left_pos in boxes_p2:
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.5), box_width, box_height)
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = RGBColor(203, 213, 225)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = 'Helvetica'
        p.font.bold = True
        p.font.size = Pt(16)
        p.font.color.rgb = NAVY
        p.space_after = Pt(12)
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = 'Helvetica'
        p2.font.size = Pt(13)
        p2.font.color.rgb = DARK

    # SLIDE 7
    slide = prs.slides.add_slide(blank_slide_layout)
    add_header(slide, "4. Best API Plan & Strategy for Personal Usage", "Recommended multi-provider configuration for maximum ROI and zero friction")

    tb = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    strategies = [
        ("1. Primary Free Tier & Long-Context: Google AI Studio (Gemini)", "â¢ Why: Generous free developer rate limits and massive 1Mâ2M context windows make it unbeatable for research, document analysis, and zero-cost prototyping."),
        ("2. Ultra-Low Cost Production & Coding: DeepSeek API", "â¢ Why: Pay-as-you-go pricing at $0.15 / $0.60 per 1M tokens delivers elite intelligence for programmatic scripts and coding assistants at 1/10th the cost of US commercial labs."),
        ("3. Sandbox & Exploration: OpenRouter", "â¢ Why: Instant access to 25+ free models and a unified API key to toggle between OpenAI, Anthropic, and open-source models effortlessly.")
    ]

    for title, desc in strategies:
        p = tf.add_paragraph()
        p.space_after = Pt(12)
        run1 = p.add_run()
        run1.text = title + "\n"
        run1.font.name = 'Helvetica'
        run1.font.bold = True
        run1.font.size = Pt(15)
        run1.font.color.rgb = NAVY
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = 'Helvetica'
        run2.font.size = Pt(13)
        run2.font.color.rgb = DARK

    callout = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.0))
    callout.fill.solid()
    callout.fill.fore_color.rgb = RGBColor(235, 248, 255)
    callout.line.color.rgb = BLUE
    ctf = callout.text_frame
    ctf.word_wrap = True
    ctf.margin_left = Inches(0.3)
    ctf.margin_top = Inches(0.15)
    cp = ctf.paragraphs[0]
    cp.text = "Summary Recommendation: Start entirely free with Google AI Studio for massive context tasks and prototyping. Add a small $10 prepaid balance to DeepSeek API for ultra-cheap programmatic agents and coding workflows."
    cp.font.name = 'Helvetica'
    cp.font.size = Pt(13)
    cp.font.bold = True
    cp.font.color.rgb = NAVY

    prs.save(filename)
    print(f"Successfully generated presentation: {filename}")

if __name__ == "__main__":
    create_presentation()
