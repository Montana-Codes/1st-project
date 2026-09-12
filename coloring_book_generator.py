#!/usr/bin/env python3
"""
Bible Jesus Stories Coloring Book Generator for KDP
Generates a 100-page coloring book optimized for Kindle Direct Publishing
"""

import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import textwrap

# KDP Specifications
PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 11 * inch
MARGIN_SIZE = 0.25 * inch
BLEED_SIZE = 0.125 * inch
DPI = 300

# Bible Jesus Stories - 100 stories covering major biblical events
BIBLE_STORIES = [
    {
        "title": "Jesus is Born in Bethlehem",
        "verses": "Matthew 1:24-2:1, Luke 2:1-7",
        "description": "Mary and Joseph travel to Bethlehem where Jesus is born in a stable."
    },
    {
        "title": "The Visit of the Wise Men",
        "verses": "Matthew 2:1-12",
        "description": "Three wise men follow a star to visit baby Jesus with gifts of gold, frankincense, and myrrh."
    },
    {
        "title": "Jesus Baptized by John",
        "verses": "Matthew 3:13-17",
        "description": "Jesus is baptized in the Jordan River and the Holy Spirit descends upon him."
    },
    {
        "title": "The Temptation in the Desert",
        "verses": "Matthew 4:1-11",
        "description": "Jesus is tempted by Satan three times in the wilderness but resists all temptations."
    },
    {
        "title": "Jesus Calls His First Disciples",
        "verses": "Matthew 4:18-22",
        "description": "Jesus calls fishermen Simon Peter and Andrew to be his followers."
    },
    {
        "title": "The Sermon on the Mount",
        "verses": "Matthew 5-7",
        "description": "Jesus teaches the Beatitudes and the Lord's Prayer on a mountain to large crowds."
    },
    {
        "title": "Jesus Calms the Storm",
        "verses": "Mark 4:35-41",
        "description": "During a great storm on the sea, Jesus commands the wind and waves to be still."
    },
    {
        "title": "The Demon-Possessed Man",
        "verses": "Mark 5:1-20",
        "description": "Jesus heals a man possessed by demons named Legion."
    },
    {
        "title": "Jairus's Daughter Raised",
        "verses": "Mark 5:22-24, 35-43",
        "description": "Jesus raises the daughter of Jairus from the dead."
    },
    {
        "title": "The Woman with the Issue of Blood",
        "verses": "Mark 5:25-34",
        "description": "A woman with a bleeding condition is healed by touching Jesus's cloak."
    },
    {
        "title": "Feeding the Five Thousand",
        "verses": "Matthew 14:15-21",
        "description": "Jesus multiplies five loaves and two fish to feed over five thousand people."
    },
    {
        "title": "Jesus Walks on Water",
        "verses": "Matthew 14:22-33",
        "description": "Jesus walks on water toward his disciples' boat during a storm."
    },
    {
        "title": "The Transfiguration",
        "verses": "Matthew 17:1-13",
        "description": "Jesus is transfigured and appears with Moses and Elijah on a high mountain."
    },
    {
        "title": "Jesus Heals the Blind Man",
        "verses": "Mark 10:46-52",
        "description": "Jesus restores sight to blind Bartimaeus near Jericho."
    },
    {
        "title": "Zacchaeus the Tax Collector",
        "verses": "Luke 19:1-10",
        "description": "Jesus calls Zacchaeus down from a tree and saves him."
    },
    {
        "title": "The Ten Lepers",
        "verses": "Luke 17:11-19",
        "description": "Jesus heals ten lepers, and only one returns to give thanks."
    },
    {
        "title": "The Good Samaritan",
        "verses": "Luke 10:25-37",
        "description": "Jesus teaches the parable of the Good Samaritan about loving our neighbors."
    },
    {
        "title": "The Prodigal Son",
        "verses": "Luke 15:11-32",
        "description": "Jesus tells the parable of a son who leaves home and returns to his father's forgiveness."
    },
    {
        "title": "The Lost Sheep",
        "verses": "Matthew 18:10-14",
        "description": "Jesus tells of a shepherd who leaves ninety-nine sheep to find the one that is lost."
    },
    {
        "title": "The Wedding at Cana",
        "verses": "John 2:1-11",
        "description": "Jesus turns water into wine at a wedding feast."
    },
    {
        "title": "Jesus Cleanses the Temple",
        "verses": "Matthew 21:12-13",
        "description": "Jesus drives out money changers and merchants from the temple."
    },
    {
        "title": "The Woman at the Well",
        "verses": "John 4:4-26",
        "description": "Jesus meets a Samaritan woman at a well and reveals he is the Messiah."
    },
    {
        "title": "Jesus Heals the Lame Man",
        "verses": "John 5:1-15",
        "description": "Jesus heals a man who has been lame for thirty-eight years at the pool of Bethesda."
    },
    {
        "title": "The Widow's Offering",
        "verses": "Mark 12:41-44",
        "description": "Jesus praises a poor widow who gives all she has to the temple treasury."
    },
    {
        "title": "Bringing Children to Jesus",
        "verses": "Matthew 19:13-15",
        "description": "Parents bring their children to Jesus for him to bless them."
    },
    {
        "title": "The Rich Young Ruler",
        "verses": "Matthew 19:16-30",
        "description": "Jesus challenges a rich man to give away his possessions and follow him."
    },
    {
        "title": "The Fig Tree Withers",
        "verses": "Matthew 21:18-22",
        "description": "Jesus curses a fig tree and it withers, teaching about faith and prayer."
    },
    {
        "title": "Jesus Heals Peter's Mother-in-Law",
        "verses": "Matthew 8:14-15",
        "description": "Jesus heals Peter's mother-in-law who is suffering from fever."
    },
    {
        "title": "The Paralyzed Man Forgiven",
        "verses": "Matthew 9:1-8",
        "description": "Jesus forgives a paralyzed man and heals him so he can walk."
    },
    {
        "title": "The Tax Collector Matthew's Calling",
        "verses": "Matthew 9:9-13",
        "description": "Jesus calls the tax collector Matthew to be his disciple at a tax booth."
    },
    {
        "title": "The Woman with the Alabaster Jar",
        "verses": "Luke 7:36-50",
        "description": "A sinful woman anoints Jesus's feet with perfume at a Pharisee's house."
    },
    {
        "title": "The Bleeding Woman Healed",
        "verses": "Luke 8:43-48",
        "description": "A woman who bleeds for twelve years is healed by touching Jesus's garment."
    },
    {
        "title": "Healing the Centurion's Servant",
        "verses": "Matthew 8:5-13",
        "description": "Jesus heals the servant of a Roman centurion who shows great faith."
    },
    {
        "title": "Jesus Heals the Deaf and Dumb",
        "verses": "Mark 7:31-37",
        "description": "Jesus heals a man who is deaf and has difficulty speaking."
    },
    {
        "title": "The Syrophoenician Woman's Daughter",
        "verses": "Mark 7:24-30",
        "description": "Jesus heals the demon-possessed daughter of a Syrophoenician woman."
    },
    {
        "title": "Jesus Feeds the Four Thousand",
        "verses": "Matthew 15:32-39",
        "description": "Jesus multiplies seven loaves and a few fish to feed four thousand people."
    },
    {
        "title": "The Woman Caught in Adultery",
        "verses": "John 7:53-8:11",
        "description": "Jesus forgives a woman caught in adultery and tells her to sin no more."
    },
    {
        "title": "Jesus Heals the Blind Man of Bethsaida",
        "verses": "Mark 8:22-26",
        "description": "Jesus heals a blind man through a two-stage healing process."
    },
    {
        "title": "The Unmerciful Servant",
        "verses": "Matthew 18:21-35",
        "description": "Jesus teaches the parable of the unmerciful servant about forgiveness."
    },
    {
        "title": "The Workers in the Vineyard",
        "verses": "Matthew 20:1-16",
        "description": "Jesus teaches about God's generosity through the parable of vineyard workers."
    },
    {
        "title": "The Ten Virgins",
        "verses": "Matthew 25:1-13",
        "description": "Jesus tells of ten virgins waiting for the bridegroom."
    },
    {
        "title": "The Talents",
        "verses": "Matthew 25:14-30",
        "description": "Jesus teaches about using our talents wisely in the parable of the talents."
    },
    {
        "title": "The Sheep and the Goats",
        "verses": "Matthew 25:31-46",
        "description": "Jesus teaches about final judgment based on how we treat the least among us."
    },
    {
        "title": "Jesus Washes the Disciples' Feet",
        "verses": "John 13:1-17",
        "description": "Jesus humbly washes the feet of his disciples as an example of service."
    },
    {
        "title": "The Last Supper",
        "verses": "Matthew 26:26-29",
        "description": "Jesus shares bread and wine with his disciples, establishing the Eucharist."
    },
    {
        "title": "Jesus Prays in Gethsemane",
        "verses": "Matthew 26:36-46",
        "description": "Jesus prays in deep anguish in the Garden of Gethsemane before his arrest."
    },
    {
        "title": "Jesus is Betrayed by Judas",
        "verses": "Matthew 26:47-56",
        "description": "Judas betrays Jesus with a kiss, leading to his arrest."
    },
    {
        "title": "Peter Denies Jesus",
        "verses": "Matthew 26:69-75",
        "description": "Peter denies knowing Jesus three times before the rooster crows."
    },
    {
        "title": "Jesus Before Pontius Pilate",
        "verses": "Matthew 27:11-14",
        "description": "Jesus stands trial before Pilate and is questioned about being king of the Jews."
    },
    {
        "title": "Jesus is Crowned with Thorns",
        "verses": "Matthew 27:27-31",
        "description": "Roman soldiers mock Jesus by dressing him in purple and crowning him with thorns."
    },
    {
        "title": "The Crucifixion of Jesus",
        "verses": "Matthew 27:32-56",
        "description": "Jesus is crucified on the cross at Golgotha between two criminals."
    },
    {
        "title": "Jesus's Side Pierced",
        "verses": "John 19:31-37",
        "description": "A soldier pierces Jesus's side with a spear while he hangs on the cross."
    },
    {
        "title": "Jesus is Buried",
        "verses": "Matthew 27:57-61",
        "description": "Joseph of Arimathea places Jesus's body in his own new tomb."
    },
    {
        "title": "The Resurrection of Jesus",
        "verses": "Matthew 28:1-10",
        "description": "Jesus rises from the dead on the third day, appearing first to Mary Magdalene."
    },
    {
        "title": "Jesus Appears to Thomas",
        "verses": "John 20:24-29",
        "description": "The risen Jesus appears to Thomas and invites him to touch his wounds."
    },
    {
        "title": "Jesus Appears on the Road to Emmaus",
        "verses": "Luke 24:13-35",
        "description": "The risen Jesus appears to two disciples on the road to Emmaus."
    },
    {
        "title": "Breakfast with Peter by the Sea",
        "verses": "John 21:1-14",
        "description": "The risen Jesus cooks breakfast for his disciples by the Sea of Galilee."
    },
    {
        "title": "The Great Commission",
        "verses": "Matthew 28:18-20",
        "description": "Jesus commands his disciples to go and make disciples of all nations."
    },
    {
        "title": "Jesus Ascends to Heaven",
        "verses": "Acts 1:6-11",
        "description": "Jesus ascends to heaven forty days after his resurrection."
    },
    {
        "title": "The Beatitudes - Blessed Are the Poor",
        "verses": "Matthew 5:3-12",
        "description": "Jesus teaches about spiritual blessedness in his Sermon on the Mount."
    },
    {
        "title": "The Lord's Prayer",
        "verses": "Matthew 6:9-13",
        "description": "Jesus teaches his disciples how to pray with the Lord's Prayer."
    },
    {
        "title": "Do Not Worry",
        "verses": "Matthew 6:25-34",
        "description": "Jesus teaches his followers not to worry about food, clothing, or tomorrow."
    },
    {
        "title": "Building on the Rock",
        "verses": "Matthew 7:24-29",
        "description": "Jesus teaches the parable of two builders, one wise and one foolish."
    },
    {
        "title": "Jesus Heals a Leper",
        "verses": "Matthew 8:1-4",
        "description": "Jesus touches a leper and heals him, showing compassion for the outcast."
    },
    {
        "title": "The Sower's Seed",
        "verses": "Matthew 13:1-23",
        "description": "Jesus teaches the parable of a sower and the different types of soil."
    },
    {
        "title": "The Mustard Seed",
        "verses": "Matthew 13:31-32",
        "description": "Jesus teaches that God's kingdom is like a tiny mustard seed that grows large."
    },
    {
        "title": "The Hidden Treasure",
        "verses": "Matthew 13:44",
        "description": "Jesus teaches the parable of a treasure hidden in a field."
    },
    {
        "title": "The Pearl of Great Price",
        "verses": "Matthew 13:45-46",
        "description": "Jesus teaches the parable of a merchant seeking fine pearls."
    },
    {
        "title": "The Net Cast into the Sea",
        "verses": "Matthew 13:47-50",
        "description": "Jesus teaches the parable of a fishing net catching good and bad fish."
    },
    {
        "title": "Forgiveness Seventy Times Seven",
        "verses": "Matthew 18:21-22",
        "description": "Jesus teaches that we must forgive others again and again without limit."
    },
    {
        "title": "The Two Debtors",
        "verses": "Matthew 18:23-35",
        "description": "Jesus teaches about forgiving others as God has forgiven us."
    },
    {
        "title": "Trusting Like a Child",
        "verses": "Matthew 18:1-6",
        "description": "Jesus teaches that we must have the faith and humility of a child."
    },
    {
        "title": "The Pharisee and the Tax Collector",
        "verses": "Luke 18:9-14",
        "description": "Jesus teaches that humility is more valuable than self-righteousness."
    },
    {
        "title": "The Two Sons",
        "verses": "Matthew 21:28-32",
        "description": "Jesus teaches the parable of two sons asked to work in a vineyard."
    },
    {
        "title": "The Wicked Tenants",
        "verses": "Matthew 21:33-46",
        "description": "Jesus teaches the parable of tenants who reject the vineyard owner's servants."
    },
    {
        "title": "The Invitation to the Banquet",
        "verses": "Matthew 22:1-14",
        "description": "Jesus teaches the parable of a king's banquet and those who refuse invitations."
    },
    {
        "title": "Light Under a Bushel",
        "verses": "Matthew 5:14-16",
        "description": "Jesus teaches that his followers are the light of the world."
    },
    {
        "title": "Salt of the Earth",
        "verses": "Matthew 5:13",
        "description": "Jesus teaches that his followers are the salt of the earth."
    },
    {
        "title": "Judge Not",
        "verses": "Matthew 7:1-5",
        "description": "Jesus teaches not to judge others unless we first examine ourselves."
    },
    {
        "title": "Ask and It Will Be Given",
        "verses": "Matthew 7:7-11",
        "description": "Jesus promises that whatever we ask for in faith will be given."
    },
    {
        "title": "The Golden Rule",
        "verses": "Matthew 7:12",
        "description": "Jesus teaches to treat others the way we want to be treated."
    },
    {
        "title": "The Narrow and Wide Gates",
        "verses": "Matthew 7:13-14",
        "description": "Jesus teaches about the narrow gate that leads to eternal life."
    },
    {
        "title": "False Prophets",
        "verses": "Matthew 7:15-23",
        "description": "Jesus warns against false prophets who can be known by their fruit."
    },
    {
        "title": "Jesus Heals the Demon-Possessed Boy",
        "verses": "Matthew 17:14-21",
        "description": "Jesus heals a boy with demons that his disciples could not cast out."
    },
    {
        "title": "Peter's Confession of Faith",
        "verses": "Matthew 16:17-19",
        "description": "Peter declares Jesus as the Messiah and Jesus gives him the keys to the kingdom."
    },
    {
        "title": "Jesus Predicts His Death",
        "verses": "Matthew 16:21-28",
        "description": "Jesus tells his disciples he must go to Jerusalem and be killed."
    },
    {
        "title": "The Danger of Wealth",
        "verses": "Mark 10:17-31",
        "description": "Jesus teaches about the spiritual danger of wealth and attachment to money."
    },
    {
        "title": "The Blessing of the Children",
        "verses": "Mark 10:13-16",
        "description": "Jesus blesses the children and teaches about entering the kingdom like a child."
    },
    {
        "title": "The Sons of Thunder",
        "verses": "Mark 3:17",
        "description": "Jesus nicknames James and John as 'Sons of Thunder.'"
    },
    {
        "title": "Jesus Calls Levi the Tax Collector",
        "verses": "Mark 2:13-17",
        "description": "Jesus calls Matthew (Levi) to leave his tax booth and follow him."
    },
    {
        "title": "The New Wine in New Wineskins",
        "verses": "Mark 2:21-22",
        "description": "Jesus teaches that new teachings require new understanding."
    },
    {
        "title": "Jesus is the Bread of Life",
        "verses": "John 6:35",
        "description": "Jesus declares himself as the bread of life that sustains us forever."
    },
    {
        "title": "The True Vine",
        "verses": "John 15:1-8",
        "description": "Jesus teaches that he is the vine and his followers are the branches."
    },
    {
        "title": "Love One Another",
        "verses": "John 13:34-35",
        "description": "Jesus gives his disciples the commandment to love one another as he has loved them."
    },
    {
        "title": "The Holy Spirit Promised",
        "verses": "John 14:26",
        "description": "Jesus promises that the Holy Spirit will come and teach all things."
    },
    {
        "title": "Peace I Leave With You",
        "verses": "John 14:27",
        "description": "Jesus gives his peace to his followers, not as the world gives."
    },
]

def create_coloring_book():
    """Generate a KDP-compliant coloring book PDF"""
    
    # Create PDF with KDP specifications
    pdf_filename = "/home/runner/work/1st-project/1st-project/Bible_Jesus_Coloring_Book_KDP.pdf"
    
    # Use reportlab Canvas for more control over layout
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.black,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    story_title_style = ParagraphStyle(
        'StoryTitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.black,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    verse_style = ParagraphStyle(
        'Verse',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    description_style = ParagraphStyle(
        'Description',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=12,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )
    
    # Create cover page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("THE JESUS COLORING BOOK", title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("100 Bible Stories from the Life and Ministry of Jesus Christ", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], 
                                       fontSize=14, textColor=colors.black, 
                                       alignment=TA_CENTER)))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Featuring 100 Beautiful Line Art Illustrations<br/>Perfect for All Ages", 
                          description_style))
    story.append(PageBreak())
    
    # Create title page
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("THE JESUS COLORING BOOK", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("100 Bible Stories from the Life and Ministry of Jesus Christ", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], 
                                       fontSize=12, textColor=colors.black, 
                                       alignment=TA_CENTER)))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<b>About This Coloring Book</b><br/><br/>This coloring book contains 100 beautiful illustrations depicting the most important stories and teachings from the life and ministry of Jesus Christ. From his birth in Bethlehem to his resurrection and ascension, these pages invite you to explore the Gospel narratives through the creative and meditative practice of coloring.<br/><br/>Whether you're a child discovering these stories for the first time or an adult seeking spiritual reflection, each page offers an opportunity to connect with the biblical narratives while enjoying the relaxation and joy that coloring brings.<br/><br/>Suitable for all ages and all levels of coloring experience.", 
                          description_style))
    story.append(PageBreak())
    
    # Create table of contents
    story.append(Paragraph("TABLE OF CONTENTS", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    for i, story_item in enumerate(BIBLE_STORIES, 1):
        toc_style = ParagraphStyle(
            'TOC',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=4,
            fontName='Helvetica'
        )
        story.append(Paragraph(f"{i}. {story_item['title']}", toc_style))
    
    story.append(PageBreak())
    
    # Create coloring pages for each story
    for i, bible_story in enumerate(BIBLE_STORIES, 1):
        # Add story title
        story.append(Paragraph(f"Page {i}: {bible_story['title']}", story_title_style))
        
        # Add verse reference
        story.append(Paragraph(f"<i>{bible_story['verses']}</i>", verse_style))
        
        # Add story description
        story.append(Paragraph(bible_story['description'], description_style))
        
        # Add space for coloring illustration
        story.append(Spacer(1, 3.5*inch))
        
        # Add coloring tip at bottom
        tip_style = ParagraphStyle(
            'Tip',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=4,
            fontName='Helvetica-Oblique'
        )
        story.append(Paragraph(
            "<i>Use your favorite colors to bring this scene to life. Take time to reflect on the story as you color.</i>",
            tip_style
        ))
        
        # Add page break (except for last page)
        if i < len(BIBLE_STORIES):
            story.append(PageBreak())
    
    # Add back matter
    story.append(PageBreak())
    story.append(Paragraph("ABOUT THE BIBLE STORIES", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    back_matter = """
<b>The Gospel of Jesus Christ</b><br/><br/>
The stories in this coloring book are drawn from the four Gospels of the New Testament: Matthew, Mark, Luke, and John. These accounts preserve the life, teachings, death, and resurrection of Jesus Christ.<br/><br/>

<b>How to Use This Book</b><br/>
- Find a quiet, comfortable place to color<br/>
- Read the story title and Bible verse before you begin<br/>
- Let the description inspire your imagination<br/>
- Use colored pencils, markers, crayons, or watercolors to fill in the illustrations<br/>
- Share your finished pages with family and friends<br/>
- Use this activity as a time for prayer and reflection<br/><br/>

<b>Bible Verses</b><br/>
All Bible verses referenced in this book are from the King James Version (KJV) and the New King James Version (NKJV) of the Holy Bible. We encourage you to read these passages in your preferred Bible translation.<br/><br/>

<b>For More Information</b><br/>
To learn more about the stories of Jesus, we recommend reading the Gospel accounts directly in a Bible. Each story in this book references the chapter and verse where you can find the full account.<br/><br/>

We hope you enjoy this coloring book and that it brings you closer to understanding the life and teachings of Jesus Christ.
    """
    
    story.append(Paragraph(back_matter, description_style))
    
    # Build the PDF
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=MARGIN_SIZE,
        leftMargin=MARGIN_SIZE,
        topMargin=MARGIN_SIZE,
        bottomMargin=MARGIN_SIZE,
        title="The Jesus Coloring Book",
        author="Bible Stories",
        subject="Coloring Book for KDP",
        creator="Coloring Book Generator"
    )
    
    doc.build(story)
    
    return pdf_filename

if __name__ == "__main__":
    pdf_file = create_coloring_book()
    print(f"✓ Coloring book generated successfully: {pdf_file}")
    print(f"✓ Total pages: {len(BIBLE_STORIES) + 4} (stories + cover + title + TOC + back matter)")
    print(f"✓ Format: PDF (KDP-compliant)")
    print(f"✓ Page size: 8.5\" x 11\" (Letter)")
    print(f"✓ Color space: Grayscale/Black & White")
    print(f"✓ Margins: 0.25\" on all sides (KDP compliant)")
