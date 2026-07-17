import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io
import traceback

# ==========================================
# 1. PORTAL CONFIGURATION & CORPORATE THEME
# ==========================================
st.set_page_config(
    page_title="Data Analytics Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Power BI Desktop Official Color Palette Accent Hex Codes
PBI_COLORS = ["#118D95", "#3B8EA5", "#F2C811", "#E36C22", "#A23B72", "#2F5296", "#666666"]
sns.set_palette(sns.color_palette(PBI_COLORS))
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=PBI_COLORS)

# Corporate Custom CSS Injection
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button {
        background-color: #118D95 !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #0E7278 !important; }
    h1, h2, h3 { color: #252423; font-family: 'Segoe UI', sans-serif; }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #252423;
        color: #FFFFFF;
        text-align: center;
        padding: 8px 0;
        font-size: 12px;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# Title Banner
st.title("📊 Data Analytics Assistant")
st.caption("Enterprise-Grade Automated Insight Engine")

# ==========================================
# 2. SIDEBAR CONTENT & FILE UPLOADERS
# ==========================================
st.sidebar.header("📁 Step 1: Data Ingestion")
data_file = st.sidebar.file_uploader("Upload Dataset (CSV or XLSX)", type=["csv", "xlsx"])

question_file = st.sidebar.file_uploader("Upload Analysis Target Questions (TXT)", type=["txt"])

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Step 2: Engine Selection")
report_type = st.sidebar.selectbox(
    "Target Reporting Platform Environment",
    ["Power BI Style (Python Framework)", "Tableau Style (Python Framework)", "Raw Python (VS Code Component)"]
)

# Global Variables for parsed data
df = None
sheet_names = []
selected_sheet = None
questions_list = []

# Process Data Upload (Supports High Volume Rowcounts > 500,000+ rows seamlessly)
if data_file:
    try:
        if data_file.name.endswith('.csv'):
            df = pd.read_csv(data_file)
        else:
            xl = pd.ExcelFile(data_file)
            sheet_names = xl.sheet_names
            selected_sheet = st.sidebar.selectbox("Select Active Excel Sheet Workspace", sheet_names)
            df = pd.read_excel(data_file, sheet_name=selected_sheet)
        
        st.sidebar.success(f"Successfully loaded {df.shape[0]:,} rows × {df.shape[1]} columns.")
    except Exception as e:
        st.sidebar.error(f"Error parsing data file: {e}")

# Process Questions Text Input File
if question_file:
    try:
        stringio = io.StringIO(question_file.getvalue().decode("utf-8"))
        questions_list = [line.strip() for line in stringio.readlines() if line.strip()]
        st.sidebar.success(f"Parsed {len(questions_list)} operational targets.")
    except Exception as e:
        st.sidebar.error(f"Error parsing text file: {e}")

# ==========================================
# 3. INTERACTIVE TAB BED WORKSPACES
# ==========================================
tab1, tab2, tab3 = st.tabs(["💡 Code & Answer Generator", "📈 Automated Dashboard Portal", "📄 Document Export Center"])

# ------------------------------------------
# TAB 1: CODE GENERATOR (EXECUTE WITHOUT BULK DASHBOARD LOADING)
# ------------------------------------------
with tab1:
    st.header("⚡ Code Blueprint & Explicit Answer Hub")
    st.write("Extract standalone executable Python scripts optimized for VS Code environments based on target metrics.")
    
    if df is not None and len(questions_list) > 0:
        st.info("Dataset and questions validated. Review the generated code structures targeted below:")
        
        generated_snippets = []
        
        # Simple programmatic mapping to generate code based on uploaded text instructions
        for i, q in enumerate(questions_list):
            st.subheader(f"Question {i+1}: {q}")
            
            # Infer string matches to create relevant standalone analysis scripts
            q_lower = q.lower()
            code_block = ""
            
            if "distribution" in q_lower or "histogram" in q_lower or "spread" in q_lower:
                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                target_col = num_cols[0] if num_cols else df.columns[0]
                code_block = f"""# --- Code Block for Question {i+1} ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("{data_file.name}") if "{data_file.name}".endswith('.csv') else pd.read_excel("{data_file.name}", sheet_name="{selected_sheet or 0}")

plt.figure(figsize=(10, 5))
# PBI Native Teal Hex Core Accent (#118D95)
sns.histplot(data=df, x="{target_col}", kde=True, color="#118D95")
plt.title("Distribution Workspace Analysis - {target_col}")
plt.xlabel("{target_col}")
plt.ylabel("Frequency Metrics")
plt.tight_layout()
plt.show()
"""
            elif "trend" in q_lower or "over time" in q_lower or "growth" in q_lower:
                code_block = f"""# --- Code Block for Question {i+1} ---
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("{data_file.name}") if "{data_file.name}".endswith('.csv') else pd.read_excel("{data_file.name}", sheet_name="{selected_sheet or 0}")

# Identifies first available column or index grouping
plt.figure(figsize=(10, 5))
plt.plot(df.index[:100], df.iloc[:100, 0], marker='o', color="#118D95", linewidth=2)
plt.title("Time-Series Matrix Evolution Trend View")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
"""
            else:
                cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                x_col = cat_cols[0] if cat_cols else df.columns[0]
                y_col = num_cols[0] if num_cols else df.columns[-1]
                
                code_block = f"""# --- Code Block for Question {i+1} ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("{data_file.name}") if "{data_file.name}".endswith('.csv') else pd.read_excel("{data_file.name}", sheet_name="{selected_sheet or 0}")

# Aggregate top 10 elements to prevent execution canvas overflow
top_data = df.groupby("{x_col}")["{y_col}"].sum().nlargest(10).reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=top_data, x="{x_col}", y="{y_col}", color="#118D95")
plt.title(f"Top 10 Aggregate Matrix Analysis: {q}")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
"""
            st.code(code_block, language='python')
            generated_snippets.append(code_block)
            
        # Unified Master Downloadable File for Easy Copy/Paste straight to VS Code
        master_code = "\n\n".join(generated_snippets)
        st.download_button(
            label="💾 Download All Generated Code for VS Code",
            data=master_code,
            file_name="vscode_analytics_script.py",
            mime="text/x-python"
        )
    else:
        st.warning("Please upload both a Dataset and a Target Questions text file (.txt) in the sidebar to populate answers.")

# ------------------------------------------
# TAB 2: AUTOMATED DASHBOARD PORTAL
# ------------------------------------------
with tab2:
    st.header("📊 Interactive Dashboard Application Canvas")
    
    if df is not None:
        st.write("### Data Preview Grid Matrix")
        st.dataframe(df.head(10), use_container_width=True)
        
        # User Interaction Execution Trigger Button
        analyze_btn = st.button("🚀 Analyze Workspace Data")
        
        if analyze_btn:
            st.success("Execution engine initialized successfully.")
            
            # Diagnostic Key Performance Indicator (KPI) Metric Cards
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Total Ingested Data Rows", value=f"{df.shape[0]:,}")
            with col2:
                st.metric(label="Total Measured Columns", value=df.shape[1])
            with col3:
                st.metric(label="Platform Theme Mode Engine", value=report_type.split()[0])
            
            st.markdown("---")
            st.subheader("🎯 Automated Contextual Visualization Layout")
            
            # ==========================================
            # SMART TARGET VISUALIZATION ENGINE (FIXED)
            # ==========================================
            if questions_list:
                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                all_cols = df.columns.tolist()

                for idx, question in enumerate(questions_list):
                    st.write(f"#### Insight Render Area {idx+1}: *{question}*")
                    q_low = question.lower()
                    
                    active_num_col = num_cols[0] if num_cols else None
                    active_cat_col = cat_cols[0] if cat_cols else None
                    
                    for col in all_cols:
                        if col.lower() in q_low:
                            if col in num_cols:
                                active_num_col = col
                            elif col in cat_cols:
                                active_cat_col = col

                    if active_num_col == (num_cols[0] if num_cols else None) and len(num_cols) > 1:
                        active_num_col = num_cols[idx % len(num_cols)]
                    if active_cat_col == (cat_cols[0] if cat_cols else None) and len(cat_cols) > 1:
                        active_cat_col = cat_cols[idx % len(cat_cols)]

                    fig, ax = plt.subplots(figsize=(10, 4.5))
                    
                    if "distribution" in q_low or "spread" in q_low or "histogram" in q_low:
                        if active_num_col:
                            sns.histplot(data=df, x=active_num_col, kde=True, ax=ax, color="#118D95")
                            ax.set_title(f"Distribution Profile: {active_num_col}", fontsize=12, fontweight='bold')
                        else:
                            ax.text(0.5, 0.5, "Requires numeric values.", ha='center', va='center')
                            
                    elif "trend" in q_low or "time" in q_low or "growth" in q_low or "over year" in q_low:
                        if active_num_col:
                            sample_size = min(len(df), 500)
                            ax.plot(df.index[:sample_size], df[active_num_col].iloc[:sample_size], color="#E36C22", linewidth=2)
                            ax.set_title(f"Timeline Performance Metrics: {active_num_col}", fontsize=12, fontweight='bold')
                        else:
                            ax.text(0.5, 0.5, "Requires scale values.", ha='center', va='center')
                            
                    else:
                        if active_cat_col and active_num_col:
                            top_10 = df.groupby(active_cat_col)[active_num_col].sum().nlargest(10).reset_index()
                            chart_color = PBI_COLORS[idx % len(PBI_COLORS)]
                            sns.barplot(data=top_10, x=active_cat_col, y=active_num_col, ax=ax, color=chart_color)
                            plt.xticks(rotation=35, ha='right')
                            ax.set_title(f"Top 10 Metrics: {active_num_col} broken down by {active_cat_col}", fontsize=12, fontweight='bold')
                        else:
                            ax.text(0.5, 0.5, "Variables structure mismatch.", ha='center', va='center')
                    
                    ax.set_facecolor('#F8F9FA')
                    fig.patch.set_facecolor('#FFFFFF')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['left'].set_color('#D2D2D2')
                    ax.spines['bottom'].set_color('#D2D2D2')
                    plt.tight_layout()
                    st.pyplot(fig)
            else:
                # Default dashboard template falls back here if zero text operational rules are uploaded
                st.info("No text configuration targets supplied. Defaulting to general structure parsing.")
                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                if len(num_cols) >= 2:
                    fig, ax = plt.subplots(figsize=(10, 4))
                    sns.scatterplot(data=df.iloc[:2000], x=num_cols[0], y=num_cols[1], color="#118D95", alpha=0.7, ax=ax)
                    ax.set_title(f"Cross-Variable Linear Matrix Correlation Mapping: {num_cols[0]} vs {num_cols[1]}")
                    st.pyplot(fig)
    else:
        st.info("Please inject an enterprise CSV or multi-sheet Excel asset file via the configuration workspace to deploy layouts.")

# ------------------------------------------
# TAB 3: DOCUMENT EXPORT CENTER
# ------------------------------------------
with tab3:
    st.header("📄 Consolidated PDF Report Compiler Engine")
    st.write("Generate clean corporate PDF print files using ReportLab modules, bypassing standard browser print rendering failures.")
    
    if df is not None:
        if st.button("🛠️ Assemble Document and Verify Constraints"):
            try:
                pdf_buffer = io.BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
                story = []
                
                styles = getSampleStyleSheet()
                title_style = ParagraphStyle(
                    'CorporateHeader',
                    parent=styles['Heading1'],
                    fontName='Helvetica-Bold',
                    fontSize=24,
                    textColor=colors.HexColor('#252423'),
                    spaceAfter=15
                )
                
                body_style = ParagraphStyle(
                    'CorporateBody',
                    parent=styles['BodyText'],
                    fontName='Helvetica',
                    fontSize=10,
                    textColor=colors.HexColor('#666666'),
                    spaceAfter=10
                )
                
                # Assemble Structural Content Components
                story.append(Paragraph("Data Analytics Assistant Executive Report", title_style))
                story.append(Paragraph(f"Reporting Architecture Engine Target Profile: {report_type}", body_style))
                story.append(Spacer(1, 15))
                
                # Append high level structural descriptive matrix
                story.append(Paragraph("Summary Assessment Meta-Data Metrics Table", styles['Heading2']))
                summary_matrix = [
                    ["Metric Scope Descriptor", "Evaluated System Target Value"],
                    ["Row Records Count Checked", f"{df.shape[0]:,}"],
                    ["Variable Array Elements Flagged", str(df.shape[1])],
                    ["File Source Context Signature", str(data_file.name)]
                ]
                
                t = Table(summary_matrix, colWidths=[200, 250])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#118D95')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#FFFFFF')),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0,0), (-1,0), 8),
                    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8F9FA')),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D2D2D2')),
                    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                    ('FONTSIZE', (0,0), (-1,-1), 9),
                ]))
                story.append(t)
                
                # Document build action
                doc.build(story)
                pdf_data = pdf_buffer.getvalue()
                
                st.success("PDF Compiled cleanly without compilation errors.")
                st.download_button(
                    label="📥 Download Official Certified PDF Report",
                    data=pdf_data,
                    file_name="Data_Analytics_Assistant_Report.pdf",
                    mime="application/pdf"
                )
            except Exception as pdf_ex:
                st.error("Error creating PDF artifact file components.")
                st.text(traceback.format_exc())
    else:
        st.warning("Data loading requirements missing. Establish connections before rendering exports.")

# ==========================================
# 4. STATIC FOOTER LEGAL BLOCK CONTROLS
# ==========================================
st.markdown(
    """
    <div class="footer">
        <p>© 2026 DEBANJAN SENGUPTA. All Rights Reserved. Proprietary Corporate Platform Engine.</p>
    </div>
    """, 
    unsafe_allow_html=True
)
