import streamlit as st
import requests
import subprocess
import tempfile
import os
import pandas as pd
import sys
import time


# Set page config
st.set_page_config(
    page_title="Flight Data Analysis Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .status-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .status-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .code-container {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .query-container {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.375rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def analyze_flight_data(query, flight_bookings_file, airline_mapping_file, api_url="http://localhost:8000/analyze/"):
    """
    Make request to flight analysis API
    """
    try:
        files = {
            'flight_bookings': flight_bookings_file,
            'airline_mapping': airline_mapping_file,
        }
        
        params = {
            'query': query
        }
        
        response = requests.post(api_url, files=files, params=params, timeout=300)
        response.raise_for_status()
        
        return True, response.json()
        
    except Exception as e:
        return False, str(e)

def extract_required_imports(code):
    """
    Extract required imports from agent code and return installation commands
    """
    common_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy', 
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'statsmodels': 'statsmodels',
        'scipy': 'scipy',
        'sklearn': 'scikit-learn',
        'plotly': 'plotly',
        'dash': 'dash',
        'bokeh': 'bokeh',
        'altair': 'altair',
        'folium': 'folium',
        'geopandas': 'geopandas',
        'networkx': 'networkx',
        'beautifulsoup4': 'beautifulsoup4',
        'requests': 'requests',
        'openpyxl': 'openpyxl',
        'xlrd': 'xlrd',
        'sqlalchemy': 'sqlalchemy',
        'psycopg2': 'psycopg2-binary',
        'pymongo': 'pymongo',
        'redis': 'redis',
        'tensorflow': 'tensorflow',
        'torch': 'torch',
        'transformers': 'transformers',
        'xgboost': 'xgboost',
        'lightgbm': 'lightgbm',
        'catboost': 'catboost'
    }
    
    required_packages = set()
    
    # Look for import statements in the code
    import re
    import_patterns = [
        r'import\s+(\w+)',
        r'from\s+(\w+)\s+import',
        r'import\s+(\w+)\s+as\s+\w+'
    ]
    
    for pattern in import_patterns:
        matches = re.findall(pattern, code)
        for match in matches:
            if match in common_packages:
                required_packages.add(common_packages[match])
    
    return list(required_packages)

def create_analysis_script(agent_code, flight_bookings_path, airline_mapping_path):
    """
    Create the complete analysis script
    """
    required_packages = extract_required_imports(agent_code)
    
    # Create package installation section
    package_install_section = ""
    for package in required_packages:
        package_install_section += f"""
try:
    if '{package}' == 'scikit-learn':
        import sklearn
    elif '{package}' == 'beautifulsoup4':
        import bs4
    elif '{package}' == 'psycopg2-binary':
        import psycopg2
    else:
        __import__('{package.replace('-', '_')}')
except ImportError:
    print("Installing {package}...")
    install_package('{package}')
"""

    complete_script = f"""# -*- coding: utf-8 -*-
import sys
import subprocess
import warnings
import os
warnings.filterwarnings('ignore')

# Set encoding for Windows compatibility
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def install_package(package_name):
    \"\"\"Install a package using pip\"\"\"
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"[SUCCESS] Successfully installed {{package_name}}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install {{package_name}}: {{e}}")
        raise

# Import required packages with auto-installation
print("Loading required packages...")

try:
    import pandas as pd
except ImportError:
    print("Installing pandas...")
    install_package('pandas')
    import pandas as pd

try:
    import numpy as np
except ImportError:
    print("Installing numpy...")
    install_package('numpy')
    import numpy as np

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
except ImportError:
    print("Installing matplotlib...")
    install_package('matplotlib')
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')

try:
    import seaborn as sns
except ImportError:
    print("Installing seaborn...")
    install_package('seaborn')
    import seaborn as sns

try:
    import statsmodels.api as sm
except ImportError:
    print("Installing statsmodels...")
    install_package('statsmodels')
    import statsmodels.api as sm

# Additional common packages that might be needed
try:
    import scipy
except ImportError:
    try:
        print("Installing scipy...")
        install_package('scipy')
        import scipy
    except:
        print("Warning: scipy installation failed, some functions may not work")

try:
    import sklearn
except ImportError:
    try:
        print("Installing scikit-learn...")
        install_package('scikit-learn')
        import sklearn
    except:
        print("Warning: scikit-learn installation failed, some functions may not work")

print("[SUCCESS] All packages loaded successfully!")

# Install additional packages detected from agent code
{package_install_section}

# Load the datasets
flight_bookings_path = r"{flight_bookings_path}"
airline_mapping_path = r"{airline_mapping_path}"

# Read the flight bookings data
df_name = pd.read_csv(flight_bookings_path)
print("Dataset loaded successfully!")
print(f"Dataset shape: {{df_name.shape}}")
print(f"Columns: {{list(df_name.columns)}}")

# Display first few rows
print("\\nFirst 5 rows:")
print(df_name.head())

# Execute the agent's code
{agent_code.strip()}

# Display results
print("\\nBooking trends analysis completed!")
if 'monthly_bookings' in locals():
    print("\\nMonthly booking trends:")
    print(monthly_bookings)
    
    # Save results to CSV
    monthly_bookings.to_csv('monthly_booking_trends.csv', index=False)
    print("\\nResults saved to 'monthly_booking_trends.csv'")

# Show basic statistics
if 'df_last_year' in locals():
    print(f"\\nTotal bookings in the last year: {{len(df_last_year)}}")
    print(f"Date range: {{df_last_year['departure_dt'].min()}} to {{df_last_year['departure_dt'].max()}}")

# Display the plot if decomposition was performed
if 'decomposition' in locals():
    plt.tight_layout()
    plt.savefig('booking_trends_decomposition.png', dpi=300, bbox_inches='tight')
    print("\\nDecomposition plot saved as 'booking_trends_decomposition.png'")

print("\\nAnalysis completed successfully!")
"""
    return complete_script

def execute_analysis_script(script_content):
    """
    Execute the analysis script and capture output
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(script_content)
        temp_file_path = temp_file.name
    
    try:
        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=600,
            cwd=os.getcwd(),
            env=dict(os.environ, PYTHONUNBUFFERED='1', PYTHONIOENCODING='utf-8')
        )
        
        return True, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return False, "", "Script execution timed out after 10 minutes"
    except Exception as e:
        return False, "", f"Error executing script: {str(e)}"
    finally:
        try:
            os.unlink(temp_file_path)
        except:
            pass

def display_file_info(uploaded_file):
    """Display information about uploaded file"""
    if uploaded_file is not None:
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**File size:** {uploaded_file.size} bytes")
        st.write(f"**File type:** {uploaded_file.type}")

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary location"""
    if uploaded_file is not None:
        # Create a temporary file
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return temp_path
    return None

def main():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>✈️ Flight Data Analysis Assistant</h1>
        <p>Intelligent analysis of flight booking data with automatic code generation and execution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📁 File Upload")
        
        # File uploads
        flight_bookings_file = st.file_uploader(
            "Upload Flight Bookings CSV",
            type=['csv'],
            help="Upload your flight bookings dataset"
        )
        
        airline_mapping_file = st.file_uploader(
            "Upload Airline Mapping CSV",
            type=['csv'],
            help="Upload your airline ID to name mapping file"
        )
        
        st.header("⚙️ Configuration")
        
        # API URL configuration
        api_url = st.text_input(
            "API URL",
            value="http://localhost:8000/analyze/",
            help="URL of the flight analysis API"
        )
        
        # Pre-install packages option
        pre_install = st.checkbox(
            "Pre-install common packages",
            value=True,
            help="Install common data science packages before analysis"
        )
        
        st.header("📊 File Information")
        if flight_bookings_file:
            st.subheader("Flight Bookings")
            display_file_info(flight_bookings_file)
        
        if airline_mapping_file:
            st.subheader("Airline Mapping")
            display_file_info(airline_mapping_file)

    # Main content area
    st.header("🔍 Analysis Query")
    
    # Query input section
    with st.container():
        st.markdown('<div class="query-container">', unsafe_allow_html=True)
        
        query = st.text_area(
            "Enter your analysis query:",
            height=120,
            placeholder="e.g., What are the trends in flight bookings for the last year?\nAnalyze the correlation between booking date and flight price...\nWhat are the top 5 airlines by booking volume?",
            help="Describe what you want to analyze in your flight data"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.button(
                "🚀 Submit Analysis",
                type="primary",
                disabled=not (flight_bookings_file and airline_mapping_file and query.strip()),
                help="Start the analysis process" if (flight_bookings_file and airline_mapping_file and query.strip()) else "Please upload both files and enter a query",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display current query status
    if query.strip():
        st.success(f"Query ready: {query[:100]}{'...' if len(query) > 100 else ''}")
    else:
        st.info("Please enter an analysis query above")
    
    # Clear results button
    if st.button("🧹 Clear Results"):
        for key in list(st.session_state.keys()):
            if key.startswith('analysis_'):
                del st.session_state[key]
        st.rerun()

    # Analysis execution
    if submit_button and flight_bookings_file and airline_mapping_file and query.strip():
        
        # Save uploaded files
        flight_bookings_path = save_uploaded_file(flight_bookings_file)
        airline_mapping_path = save_uploaded_file(airline_mapping_file)
        
        if not flight_bookings_path or not airline_mapping_path:
            st.error("Failed to save uploaded files")
            return
        
        # Create tabs for different stages of analysis
        tab1, tab2, tab3, tab4 = st.tabs(["📡 API Call", "🔧 Code Generation", "⚡ Execution", "📈 Results"])
        
        with tab1:
            st.header("API Analysis Request")
            
            # Display the query being sent
            st.subheader("Query Submitted:")
            st.info(query)
            
            with st.spinner("Calling analysis API..."):
                # Reset file pointers
                flight_bookings_file.seek(0)
                airline_mapping_file.seek(0)
                
                success, result = analyze_flight_data(
                    query, 
                    flight_bookings_file, 
                    airline_mapping_file, 
                    api_url
                )
            
            if success:
                st.markdown('<div class="status-success">[SUCCESS] API call completed successfully!</div>', unsafe_allow_html=True)
                
                # Store result in session state
                st.session_state.analysis_result = result
                
                # Display API response
                with st.expander("🔍 View API Response", expanded=False):
                    st.json(result)
                
            else:
                st.markdown(f'<div class="status-error">[ERROR] API call failed: {result}</div>', unsafe_allow_html=True)
                return
        
        with tab2:
            st.header("Code Generation")
            
            if 'analysis_result' in st.session_state:
                result = st.session_state.analysis_result
                
                # Extract agent code
                if 'analysis_result' in result and 'code_combiner_agent' in result['analysis_result']:
                    agent_code = result['analysis_result']['code_combiner_agent']['refined_complete_code']
                    
                    # Clean the code
                    if agent_code.startswith('```python'):
                        agent_code = agent_code[9:]
                    if agent_code.endswith('```'):
                        agent_code = agent_code[:-3]
                    
                    st.markdown('<div class="status-success">[SUCCESS] Agent code extracted successfully!</div>', unsafe_allow_html=True)
                    
                    # Display the agent's code
                    with st.expander("🧠 Agent's Generated Code", expanded=True):
                        st.code(agent_code, language='python')
                    
                    # Generate complete script
                    complete_script = create_analysis_script(agent_code, flight_bookings_path, airline_mapping_path)
                    st.session_state.complete_script = complete_script
                    
                    # Display required packages
                    required_packages = extract_required_imports(agent_code)
                    if required_packages:
                        st.write("**Required packages detected:**")
                        st.write(", ".join(required_packages))
                    
                else:
                    st.markdown('<div class="status-error">[ERROR] No agent code found in API response</div>', unsafe_allow_html=True)
                    return
            else:
                st.warning("Please complete the API call first")
                return
        
        with tab3:
            st.header("Script Execution")
            
            if 'complete_script' in st.session_state:
                
                with st.spinner("Executing analysis script... This may take a few minutes."):
                    
                    # Create a progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Update progress
                    for i in range(10):
                        time.sleep(0.5)
                        progress_bar.progress((i + 1) * 10)
                        status_text.text(f"Executing analysis... {(i + 1) * 10}%")
                    
                    # Execute the script
                    success, output, error = execute_analysis_script(st.session_state.complete_script)
                    
                    progress_bar.progress(100)
                    status_text.empty()
                
                if success:
                    st.markdown('<div class="status-success">[SUCCESS] Script execution completed!</div>', unsafe_allow_html=True)
                    
                    # Store results
                    st.session_state.execution_output = output
                    st.session_state.execution_error = error
                    
                    # Display execution output
                    if output:
                        with st.expander("📋 Execution Output", expanded=True):
                            st.text(output)
                    
                    if error:
                        with st.expander("⚠️ Warnings/Errors", expanded=False):
                            st.text(error)
                
                else:
                    st.markdown(f'<div class="status-error">[ERROR] Script execution failed: {error}</div>', unsafe_allow_html=True)
                    return
            else:
                st.warning("Please complete code generation first")
                return
        
        with tab4:
            st.header("Analysis Results")
            
            if 'execution_output' in st.session_state:
                
                # Check for generated files
                results_files = []
                plot_files = []
                
                # Look for CSV files
                if os.path.exists('monthly_booking_trends.csv'):
                    results_files.append('monthly_booking_trends.csv')
                
                # Look for plot files
                if os.path.exists('booking_trends_decomposition.png'):
                    plot_files.append('booking_trends_decomposition.png')
                
                # Display results
                if results_files:
                    st.subheader("📊 Generated Data Files")
                    for file in results_files:
                        try:
                            df = pd.read_csv(file)
                            st.write(f"**{file}:**")
                            st.dataframe(df)
                            
                            # Download button
                            with open(file, 'rb') as f:
                                st.download_button(
                                    label=f"📥 Download {file}",
                                    data=f.read(),
                                    file_name=file,
                                    mime='text/csv'
                                )
                        except Exception as e:
                            st.error(f"Error reading {file}: {e}")
                
                if plot_files:
                    st.subheader("📈 Generated Plots")
                    for file in plot_files:
                        try:
                            st.image(file, caption=file, use_column_width=True)
                            
                            # Download button for plots
                            with open(file, 'rb') as f:
                                st.download_button(
                                    label=f"📥 Download {file}",
                                    data=f.read(),
                                    file_name=file,
                                    mime='image/png'
                                )
                        except Exception as e:
                            st.error(f"Error displaying {file}: {e}")
                
                if not results_files and not plot_files:
                    st.info("No output files were generated. Check the execution output above for results.")
                
                # Clean up temporary files
                try:
                    for file in results_files + plot_files:
                        if os.path.exists(file):
                            os.remove(file)
                except:
                    pass
            else:
                st.warning("Please complete script execution first")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Flight Data Analysis Assistant | Built with Streamlit</p>
        <p>Upload your CSV files, enter your query, and let AI analyze your flight data!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()