import streamlit as st
from library import Library
import plotly.express as px
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
from book import Book
from member import StudentMember, FacultyMember

st.set_page_config(
    page_title="University Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialize and load the existing library data
if "library" not in st.session_state:
    library_instance = Library()
    library_instance.load_data()
    st.session_state.library = library_instance

library = st.session_state.library


# Sidebar
with st.sidebar:
    st.title("📚 University Library")
    st.caption("Library Management System")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Book Management",
            "Member Management",
            "Loan Management",
            "Reports & Analytics"
        ]
    )


# Main content


if page == "Dashboard":

    # ==========================================
    # DASHBOARD THEME
    # ==========================================

    PRIMARY = "#818CF8"
    BLUE = "#60A5FA"
    PURPLE = "#A78BFA"
    GREEN = "#34D399"
    RED = "#FB7185"
    AMBER = "#FBBF24"
    MUTED = "#94A3B8"

    st.markdown("""
    <style>
        div[data-testid="stMetric"] {
            background: rgba(99, 102, 241, 0.055);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 14px;
            padding: 20px 22px;
        }

        div[data-testid="stMetricLabel"] {
            color: #94A3B8;
            font-size: 0.9rem;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.9rem;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            min-height: 125px;
        }

        .dashboard-header {
            margin-bottom: 22px;
        }

        .dashboard-eyebrow {
            color: #818CF8;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .dashboard-title {
            font-size: 2.1rem;
            font-weight: 750;
            margin: 6px 0;
        }

        .dashboard-description {
            color: #94A3B8;
            font-size: 0.95rem;
        }

        .dashboard-section {
            font-size: 1.25rem;
            font-weight: 650;
            margin-top: 24px;
            margin-bottom: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # LOAD LIBRARY DATA
    # ==========================================

    books = library.list_books()
    members = library.list_members()
    all_loans = list(library.loans.values())

    active_loans = library.list_active_loans()
    overdue_loans = library.list_overdue_loans()

    total_titles = len(books)
    total_members = len(members)

    total_copies = sum(
        book.total_copies for book in books
    )

    available_copies = sum(
        book.available_copies for book in books
    )

    borrowed_copies = total_copies - available_copies

    total_fines = sum(
        loan.calculate_fine() for loan in overdue_loans
    )

    student_count = sum(
        member.member_type == "Student"
        for member in members
    )

    faculty_count = sum(
        member.member_type == "Faculty"
        for member in members
    )

    returned_count = sum(
        loan.status == "Returned"
        for loan in all_loans
    )

    active_not_overdue = (
        len(active_loans) - len(overdue_loans)
    )

    # ==========================================
    # DASHBOARD HEADER
    # ==========================================

    st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-eyebrow">
            LIBRARY MANAGEMENT / OVERVIEW
        </div>
        <div class="dashboard-title">
            Library Dashboard
        </div>
        <div class="dashboard-description">
            Monitor collections, memberships,
            borrowing activity and library performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # KPI CARDS
    # ==========================================

    kpi_row1 = st.columns(3, gap="medium")

    with kpi_row1[0]:
        st.metric("📚 Book Titles", f"{total_titles:,}")

    with kpi_row1[1]:
        st.metric("👥 Registered Members", f"{total_members:,}")

    with kpi_row1[2]:
        st.metric("🔄 Active Loans", f"{len(active_loans):,}")

    st.write("")

    kpi_row2 = st.columns(3, gap="medium")

    with kpi_row2[0]:
        st.metric("📖 Available Copies", f"{available_copies:,}")

    with kpi_row2[1]:
        st.metric("⏰ Overdue Loans", f"{len(overdue_loans):,}")

    with kpi_row2[2]:
        st.metric("💰 Outstanding Fines", f"৳{total_fines:,.0f}")

    # ==========================================
    # SHARED CHART STYLING
    # ==========================================

    def style_chart(fig, height=320):
        fig.update_layout(
            template="plotly_dark",
            height=height,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=12),
            margin=dict(l=12, r=12, t=20, b=15),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5
            )
        )
        return fig

    # ==========================================
    # COLLECTION OVERVIEW
    # ==========================================

    st.markdown(
        '<div class="dashboard-section">Collection Overview</div>',
        unsafe_allow_html=True
    )

    st.caption("Current inventory and membership composition")

    chart_col1, chart_col2 = st.columns(2, gap="medium")

    with chart_col1:
        with st.container(border=True):
            st.markdown("**Book Availability**")

            book_df = pd.DataFrame({
                "Status": ["Available", "Borrowed"],
                "Copies": [available_copies, borrowed_copies]
            })

            if total_copies > 0:
                fig_books = px.pie(
                    book_df,
                    names="Status",
                    values="Copies",
                    hole=0.68,
                    color="Status",
                    color_discrete_map={
                        "Available": PRIMARY,
                        "Borrowed": RED
                    }
                )

                fig_books.update_traces(
                    textinfo="percent",
                    textposition="inside",
                    hovertemplate=(
                        "%{label}<br>"
                        "%{value} copies<br>"
                        "%{percent}<extra></extra>"
                    )
                )

                fig_books.add_annotation(
                    text=f"<b>{total_copies:,}</b><br>Copies",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=17, color="#E2E8F0")
                )

                style_chart(fig_books, 300)
                st.plotly_chart(fig_books, width="stretch")
            else:
                st.info("No inventory data available.")

    with chart_col2:
        with st.container(border=True):
            st.markdown("**Member Distribution**")

            member_df = pd.DataFrame({
                "Type": ["Student", "Faculty"],
                "Count": [student_count, faculty_count]
            })

            if student_count + faculty_count > 0:
                fig_members = px.pie(
                    member_df,
                    names="Type",
                    values="Count",
                    hole=0.68,
                    color="Type",
                    color_discrete_map={
                        "Student": BLUE,
                        "Faculty": PURPLE
                    }
                )

                fig_members.update_traces(
                    textinfo="percent",
                    textposition="inside",
                    hovertemplate=(
                        "%{label}<br>"
                        "%{value} members<br>"
                        "%{percent}<extra></extra>"
                    )
                )

                fig_members.add_annotation(
                    text=f"<b>{total_members:,}</b><br>Members",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=17, color="#E2E8F0")
                )

                style_chart(fig_members, 300)
                st.plotly_chart(fig_members, width="stretch")
            else:
                st.info("No member data available.")

    # ==========================================
    # LOAN STATUS OVERVIEW
    # ==========================================

    st.markdown(
        '<div class="dashboard-section">Loan Performance</div>',
        unsafe_allow_html=True
    )

    st.caption("Current and historical loan status")

    with st.container(border=True):
        st.markdown("**Loan Status Overview**")

        loan_df = pd.DataFrame({
            "Status": [
                "Returned",
                "Active (On Time)",
                "Overdue"
            ],
            "Count": [
                returned_count,
                active_not_overdue,
                len(overdue_loans)
            ]
        })

        fig_loans = px.bar(
            loan_df,
            x="Status",
            y="Count",
            color="Status",
            text="Count",
            color_discrete_map={
                "Returned": GREEN,
                "Active (On Time)": BLUE,
                "Overdue": RED
            }
        )

        fig_loans.update_traces(
            textposition="outside",
            cliponaxis=False,
            marker_line_width=0
        )

        fig_loans.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Number of Loans",
            bargap=0.55
        )

        fig_loans.update_yaxes(
            gridcolor="rgba(148,163,184,0.12)",
            rangemode="tozero"
        )

        style_chart(fig_loans, 310)
        st.plotly_chart(fig_loans, width="stretch")

    # ==========================================
    # BORROWING ACTIVITY HEATMAP
    # ==========================================

    st.markdown(
        '<div class="dashboard-section">Borrowing Activity</div>',
        unsafe_allow_html=True
    )

    st.caption("Daily borrowing patterns across the last 365 days")

    today = date.today()
    start_date = today - timedelta(days=364)
    grid_start = start_date - timedelta(
        days=start_date.weekday()
    )

    borrow_counts = {}

    for loan in all_loans:
        borrow_day = date.fromisoformat(loan.borrow_date)

        if start_date <= borrow_day <= today:
            borrow_counts[borrow_day] = (
                borrow_counts.get(borrow_day, 0) + 1
            )

    heatmap_rows = []
    current_day = grid_start

    while current_day <= today:
        heatmap_rows.append({
            "Date": current_day,
            "Week": (current_day - grid_start).days // 7,
            "Weekday": current_day.weekday(),
            "Borrowings": borrow_counts.get(current_day, 0)
        })

        current_day += timedelta(days=1)

    heatmap_df = pd.DataFrame(heatmap_rows)

    heatmap_grid = (
        heatmap_df.pivot(
            index="Weekday",
            columns="Week",
            values="Borrowings"
        )
        .reindex(index=range(7))
    )

    date_grid = (
        heatmap_df.assign(
            DateText=heatmap_df["Date"].astype(str)
        )
        .pivot(
            index="Weekday",
            columns="Week",
            values="DateText"
        )
        .reindex(index=range(7))
    )

    # Hide days outside the requested date range
    for row in heatmap_rows:
        if row["Date"] < start_date:
            heatmap_grid.loc[
                row["Weekday"], row["Week"]
            ] = float("nan")

    month_positions = {}
    for row in heatmap_rows:
        d = row["Date"]

        if d >= start_date and d.day <= 7:
            label = d.strftime("%b %Y")
            if label not in month_positions:
                month_positions[label] = row["Week"]

    with st.container(border=True):
        st.markdown("**Daily Borrowing Calendar**")

        fig_heatmap = go.Figure(
            go.Heatmap(
                z=heatmap_grid.values,
                x=heatmap_grid.columns.tolist(),
                y=list(range(7)),
                customdata=date_grid.values,
                colorscale=[
                    [0.0, "#1E293B"],
                    [0.25, "#2563EB"],
                    [0.5, "#6366F1"],
                    [0.75, "#8B5CF6"],
                    [1.0, "#C084FC"]
                ],
                zmin=0,
                zmax=max(
                    1,
                    int(heatmap_df["Borrowings"].max())
                ),
                xgap=3,
                ygap=3,
                colorbar=dict(
                    title="Loans",
                    thickness=12,
                    len=0.75
                ),
                hovertemplate=(
                    "Date: %{customdata}<br>"
                    "Borrowings: %{z}"
                    "<extra></extra>"
                )
            )
        )

        fig_heatmap.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=list(month_positions.values()),
                ticktext=list(month_positions.keys()),
                showgrid=False,
                side="top",
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                tickmode="array",
                tickvals=list(range(7)),
                ticktext=[
                    "Mon", "Tue", "Wed",
                    "Thu", "Fri", "Sat", "Sun"
                ],
                autorange="reversed",
                showgrid=False
            )
        )

        style_chart(fig_heatmap, 280)
        st.plotly_chart(fig_heatmap, width="stretch")

        active_days = sum(
            count > 0 for count in borrow_counts.values()
        )

        period_borrowings = sum(borrow_counts.values())

        st.caption(
            f"{period_borrowings:,} borrowings across "
            f"{active_days:,} active days in the last 365 days."
        )

    # ==========================================
    # MONTHLY BORROWING TREND
    # ==========================================

    st.markdown(
        '<div class="dashboard-section">Borrowing Trends</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Monthly loan activity over the last 12 calendar months"
    )

    current_month = pd.Timestamp(today).to_period("M")

    months = pd.period_range(
        end=current_month,
        periods=12,
        freq="M"
    )

    loan_dates = pd.to_datetime(
        [loan.borrow_date for loan in all_loans]
    )

    monthly_counts = (
        pd.Series(1, index=loan_dates)
        .groupby(lambda d: d.to_period("M"))
        .sum()
        .reindex(months, fill_value=0)
    )

    trend_df = pd.DataFrame({
        "Month": months.to_timestamp(),
        "Borrowings": monthly_counts.values
    })

    with st.container(border=True):
        st.markdown("**Monthly Borrowing Activity**")

        fig_trend = go.Figure()

        fig_trend.add_trace(
            go.Scatter(
                x=trend_df["Month"],
                y=trend_df["Borrowings"],
                mode="lines+markers",
                name="Borrowings",
                line=dict(
                    color=PRIMARY,
                    width=3,
                    shape="spline",
                    smoothing=0.5
                ),
                marker=dict(
                    size=7,
                    color=PRIMARY
                ),
                fill="tozeroy",
                fillcolor="rgba(129,140,248,0.16)",
                hovertemplate=(
                    "%{x|%B %Y}<br>"
                    "Borrowings: %{y}"
                    "<extra></extra>"
                )
            )
        )

        fig_trend.update_layout(
            showlegend=False,
            hovermode="x unified",
            xaxis=dict(
                title=None,
                tickformat="%b %Y",
                dtick="M1",
                tickangle=-30,
                showgrid=False
            ),
            yaxis=dict(
                title="Borrowings",
                rangemode="tozero",
                gridcolor="rgba(148,163,184,0.12)"
            )
        )

        style_chart(fig_trend, 340)
        st.plotly_chart(fig_trend, width="stretch")

        st.caption(
            f"October 2026 and other current-month figures "
            f"represent month-to-date activity."
            if today.year == 2026 and today.month == 10
            else "The current month is shown month-to-date."
        )

    # ==========================================
    # DASHBOARD FOOTER
    # ==========================================

    st.divider()

    st.caption(
        f"Library Management System  •  "
        f"{len(all_loans):,} total loan records  •  "
        f"Updated from the current library session"
    )


elif page == "Book Management":

    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.title("📚 Book Management")
    st.caption(
        "Manage the library collection, search inventory, "
        "and register new books."
    )

    # ==========================================
    # LOAD BOOK DATA
    # ==========================================

    books = library.list_books()

    total_titles = len(books)
    total_copies = sum(book.total_copies for book in books)
    available_copies = sum(
        book.available_copies for book in books
    )

    # ==========================================
    # INVENTORY SUMMARY
    # ==========================================

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.metric("📚 Book Titles", f"{total_titles:,}")

    with col2:
        st.metric("📖 Total Copies", f"{total_copies:,}")

    with col3:
        st.metric("✅ Available Copies", f"{available_copies:,}")

    st.divider()

    # ==========================================
    # BOOK MANAGEMENT TABS
    # ==========================================

    inventory_tab, add_tab, details_tab, edit_tab, copies_tab, remove_tab = st.tabs([
        "📚 Book Inventory",
        "➕ Add New Book",
        "🔍 Book Details",
        "✏️ Edit Book",
        "📦 Manage Copies",
        "🗑️ Remove Book"
    ])

    # ==========================================
    # TAB 1: BOOK INVENTORY
    # ==========================================

    with inventory_tab:

        st.subheader("Book Inventory")
        st.caption(
            "Browse, search, and filter the library's books."
        )

        # Search and filter controls
        search_col, category_col, status_col = st.columns(
            [2, 1, 1]
        )

        with search_col:
            search_query = st.text_input(
                "Search Books",
                placeholder="Search by ID, title or author...",
                key="book_search"
            )

        with category_col:
            categories = sorted({
                book.category for book in books
            })

            selected_category = st.selectbox(
                "Category",
                ["All Categories"] + categories,
                key="book_category"
            )

        with status_col:
            selected_status = st.selectbox(
                "Availability",
                ["All Books", "Available", "Out of Stock"],
                key="book_availability"
            )

        # Apply search and filters
        filtered_books = books

        if search_query.strip():
            query = search_query.strip().lower()

            filtered_books = [
                book for book in filtered_books
                if query in book.book_id.lower()
                or query in book.title.lower()
                or query in book.author.lower()
            ]

        if selected_category != "All Categories":
            filtered_books = [
                book for book in filtered_books
                if book.category == selected_category
            ]

        if selected_status == "Available":
            filtered_books = [
                book for book in filtered_books
                if book.available_copies > 0
            ]

        elif selected_status == "Out of Stock":
            filtered_books = [
                book for book in filtered_books
                if book.available_copies == 0
            ]

        st.caption(
            f"Showing {len(filtered_books)} "
            f"of {len(books)} book titles"
        )

        # Build inventory table
        book_records = []

        for book in filtered_books:
            book_records.append({
                "Book ID": book.book_id,
                "Title": book.title,
                "Author": book.author,
                "Category": book.category,
                "Total Copies": book.total_copies,
                "Available Copies": book.available_copies,
                "Borrowed Copies": (
                    book.total_copies - book.available_copies
                )
            })

        if book_records:
            book_df = pd.DataFrame(book_records)

            st.dataframe(
                book_df,
                width="stretch",
                hide_index=True,
                height=450
            )
        else:
            st.info("No books match your search or filters.")

    # ==========================================
    # TAB 2: ADD NEW BOOK
    # ==========================================

    with add_tab:

        st.subheader("Register New Book")
        st.caption(
            "Enter the book information below. "
            "The book ID is generated automatically."
        )

        # Generate the next available book ID
        existing_ids = [
            int(book.book_id[1:])
            for book in books
            if book.book_id.startswith("B")
            and book.book_id[1:].isdigit()
        ]

        next_id = max(existing_ids, default=0) + 1
        new_book_id = f"B{next_id:03d}"

        st.info(f"📘 New Book ID: {new_book_id}")

        with st.form(
            "add_book_form",
            clear_on_submit=True
        ):

            title = st.text_input(
                "Book Title",
                placeholder="Enter the book title"
            )

            author = st.text_input(
                "Author",
                placeholder="Enter the author's name"
            )

            category = st.text_input(
                "Category",
                placeholder="e.g. Computer Science"
            )

            total_copies = st.number_input(
                "Total Copies",
                min_value=1,
                value=1,
                step=1
            )

            submitted = st.form_submit_button(
                "➕ Register Book",
                type="primary",
                width="stretch"
            )

        # Process form submission
        if submitted:

            if (
                not title.strip()
                or not author.strip()
                or not category.strip()
            ):
                st.error(
                    "Please complete all required fields."
                )

            else:
                new_book = Book(
                    new_book_id,
                    title.strip(),
                    author.strip(),
                    category.strip(),
                    int(total_copies)
                )

                if library.add_book(new_book):
                    st.success(
                        f"Book {new_book_id} registered successfully!"
                    )
                    st.balloons()
                else:
                    st.error(
                        "Failed to register the book. "
                        "Please try again."
                    )


    # ==========================================
    # TAB 3: VIEW BOOK DETAILS
    # ==========================================

    with details_tab:

        st.subheader("Book Details")
        st.caption(
            "Select a book to view its complete information "
            "and current inventory status."
        )

        if not books:
            st.info("No books are registered in the library.")

        else:
            # Create searchable book options
            book_options = {
                f"{book.book_id} — {book.title}": book.book_id
                for book in books
            }

            selected_book = st.selectbox(
                "Select Book",
                options=list(book_options.keys()),
                index=None,
                placeholder="Search by book ID or title...",
                key="details_book_selection"
            )

            if selected_book:

                book_id = book_options[selected_book]
                book = library.get_book(book_id)

                if book is None:
                    st.error("Book not found.")

                else:
                    borrowed = (
                        book.total_copies - book.available_copies
                    )

                    st.divider()

                    st.markdown(f"### 📖 {book.title}")
                    st.caption(f"Book ID: {book.book_id}")

                    info_col1, info_col2 = st.columns(2)

                    with info_col1:
                        st.markdown("**Author**")
                        st.write(book.author)

                        st.markdown("**Category**")
                        st.write(book.category)

                    with info_col2:
                        st.markdown("**Book ID**")
                        st.write(book.book_id)

                        st.markdown("**Availability Status**")

                        if book.available_copies > 0:
                            st.success("Available")
                        else:
                            st.error("Out of Stock")

                    st.markdown("#### Inventory Information")

                    copies_col1, copies_col2, copies_col3 = (
                        st.columns(3)
                    )

                    with copies_col1:
                        st.metric(
                            "Total Copies",
                            book.total_copies
                        )

                    with copies_col2:
                        st.metric(
                            "Available Copies",
                            book.available_copies
                        )

                    with copies_col3:
                        st.metric(
                            "Borrowed Copies",
                            borrowed
                        )

                    availability_percentage = (
                        book.available_copies / book.total_copies
                        if book.total_copies > 0
                        else 0
                    )

                    st.markdown("**Inventory Availability**")

                    st.progress(
                        availability_percentage,
                        text=(
                            f"{availability_percentage:.1%} "
                            "of copies available"
                        )
                    )


    # ==========================================
    # TAB 4: UPDATE BOOK INFORMATION
    # ==========================================

    with edit_tab:

        st.subheader("Update Book Information")
        st.caption(
            "Edit a book's title, author, or category. "
            "Changes are saved automatically."
        )

        if not books:
            st.info("No books available to edit.")

        else:
            book_options = {
                f"{book.book_id} — {book.title}": book.book_id
                for book in books
            }

            selected_book = st.selectbox(
                "Select Book to Edit",
                options=list(book_options.keys()),
                index=None,
                placeholder="Search by book ID or title...",
                key="edit_book_selection"
            )

            if selected_book:

                book_id = book_options[selected_book]
                book = library.get_book(book_id)

                if book is None:
                    st.error("Book not found.")

                else:
                    st.info(f"Editing Book ID: {book.book_id}")

                    with st.form(
                        f"edit_book_form_{book_id}"
                    ):

                        new_title = st.text_input(
                            "Book Title",
                            value=book.title
                        )

                        new_author = st.text_input(
                            "Author",
                            value=book.author
                        )

                        new_category = st.text_input(
                            "Category",
                            value=book.category
                        )

                        submitted = st.form_submit_button(
                            "💾 Save Changes",
                            type="primary",
                            width="stretch"
                        )

                    if submitted:

                        if not all([
                            new_title.strip(),
                            new_author.strip(),
                            new_category.strip()
                        ]):
                            st.error(
                                "All fields are required."
                            )

                        else:
                            updates = {}

                            if new_title.strip() != book.title:
                                updates["title"] = new_title.strip()

                            if new_author.strip() != book.author:
                                updates["author"] = new_author.strip()

                            if new_category.strip() != book.category:
                                updates["category"] = new_category.strip()

                            if not updates:
                                st.info("No changes were made.")

                            elif library.update_book(
                                book_id, **updates
                            ):
                                st.success(
                                    f"Book {book_id} updated successfully!"
                                )
                            else:
                                st.error(
                                    "Failed to update book information."
                                )



    # ==========================================
    # TAB 5: MANAGE BOOK COPIES
    # ==========================================

    with copies_tab:

        st.subheader("Manage Book Copies")
        st.caption(
            "Add new copies or remove existing available copies "
            "from the library inventory."
        )

        if not books:
            st.info("No books available.")

        else:
            book_options = {
                f"{book.book_id} — {book.title}": book.book_id
                for book in books
            }

            selected_book = st.selectbox(
                "Select Book",
                options=list(book_options.keys()),
                index=None,
                placeholder="Search by book ID or title...",
                key="copies_book_selection"
            )

            if selected_book:

                book_id = book_options[selected_book]
                book = library.get_book(book_id)

                if book is None:
                    st.error("Book not found.")

                else:
                    borrowed_copies = (
                        book.total_copies - book.available_copies
                    )

                    st.divider()
                    st.markdown(f"### 📖 {book.title}")
                    st.caption(f"Book ID: {book.book_id}")

                    # Current inventory metrics
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Total Copies",
                            book.total_copies
                        )

                    with col2:
                        st.metric(
                            "Available Copies",
                            book.available_copies
                        )

                    with col3:
                        st.metric(
                            "Borrowed Copies",
                            borrowed_copies
                        )

                    st.divider()

                    # Choose inventory operation
                    operation = st.radio(
                        "Inventory Operation",
                        ["➕ Add Copies", "➖ Remove Copies"],
                        horizontal=True,
                        key="copies_operation"
                    )

                    if operation == "➕ Add Copies":

                        st.caption(
                            "New copies will increase both the total "
                            "and available inventory."
                        )

                        with st.form("add_copies_form"):

                            quantity = st.number_input(
                                "Number of Copies to Add",
                                min_value=1,
                                value=1,
                                step=1
                            )

                            submitted = st.form_submit_button(
                                "➕ Add Copies",
                                type="primary",
                                width="stretch"
                            )

                        if submitted:

                            if library.add_book_copies(
                                book_id, int(quantity)
                            ):
                                st.success(
                                    f"Successfully added {quantity} "
                                    f"copies to {book_id}!"
                                )
                                st.info(
                                    "Inventory updated. Refresh or "
                                    "interact with the page to see "
                                    "the latest totals."
                                )

                            else:
                                st.error(
                                    "Unable to add copies."
                                )

                    else:

                        st.caption(
                            "Only available copies can be removed. "
                            "Borrowed copies must be returned first."
                        )

                        if book.available_copies == 0:

                            st.warning(
                                "No available copies can be removed "
                                "from this book."
                            )

                        else:

                            with st.form("remove_copies_form"):

                                quantity = st.number_input(
                                    "Number of Copies to Remove",
                                    min_value=1,
                                    max_value=book.available_copies,
                                    value=1,
                                    step=1
                                )

                                submitted = st.form_submit_button(
                                    "➖ Remove Copies",
                                    type="primary",
                                    width="stretch"
                                )

                            if submitted:

                                if library.remove_book_copies(
                                    book_id, int(quantity)
                                ):
                                    st.success(
                                        f"Successfully removed "
                                        f"{quantity} copies from "
                                        f"{book_id}!"
                                    )
                                    st.info(
                                        "Inventory updated. Refresh "
                                        "or interact with the page "
                                        "to see the latest totals."
                                    )

                                else:
                                    st.error(
                                        "Unable to remove copies. "
                                        "Check inventory restrictions."
                                    )



    # ==========================================
    # TAB 6: REMOVE BOOK
    # ==========================================

    with remove_tab:

        st.subheader("Remove Book")
        st.caption(
            "Permanently remove a book from the library inventory."
        )

        if not books:
            st.info("No books available to remove.")

        else:
            book_options = {
                f"{book.book_id} — {book.title}": book.book_id
                for book in books
            }

            selected_book = st.selectbox(
                "Select Book to Remove",
                options=list(book_options.keys()),
                index=None,
                placeholder="Search by book ID or title...",
                key="remove_book_selection"
            )

            if selected_book:

                book_id = book_options[selected_book]
                book = library.get_book(book_id)

                if book is None:
                    st.error("Book not found.")

                else:
                    borrowed_copies = (
                        book.total_copies - book.available_copies
                    )

                    st.divider()

                    st.markdown(f"### 📖 {book.title}")
                    st.write(f"**Book ID:** {book.book_id}")
                    st.write(f"**Author:** {book.author}")
                    st.write(f"**Category:** {book.category}")

                    col1, col2, col3 = st.columns(3)

                    col1.metric("Total Copies", book.total_copies)
                    col2.metric(
                        "Available Copies",
                        book.available_copies
                    )
                    col3.metric("Borrowed Copies", borrowed_copies)

                    # Check for active loans
                    active_loans = [
                        loan for loan in library.list_active_loans()
                        if loan.book_id == book_id
                    ]

                    if active_loans or borrowed_copies > 0:

                        st.error(
                            "This book cannot be removed because "
                            "it has borrowed copies or active loans."
                        )

                        st.info(
                            "All borrowed copies must be returned "
                            "before removing this book."
                        )

                    else:

                        st.warning(
                            "This action permanently removes the "
                            "book from the inventory. "
                            "It cannot be undone."
                        )

                        with st.form(
                            f"remove_book_form_{book_id}"
                        ):

                            confirmed = st.checkbox(
                                "I understand and want to "
                                "permanently remove this book."
                            )

                            submitted = st.form_submit_button(
                                "🗑️ Permanently Remove Book",
                                type="primary",
                                width="stretch"
                            )

                        if submitted:

                            if not confirmed:
                                st.error(
                                    "Please confirm deletion first."
                                )

                            elif library.remove_book(book_id):
                                st.success(
                                    f"Book {book_id} removed successfully!"
                                )

                            else:
                                st.error(
                                    "Unable to remove this book. "
                                    "Check whether it has existing loans."
                                )


elif page == "Member Management":

    st.title("👥 Member Management")
    st.caption(
        "Register members, manage accounts, and review borrowing history."
    )

    members = library.list_members()

    total_members = len(members)
    student_count = sum(
        m.member_type.lower() == "student" for m in members
    )
    faculty_count = sum(
        m.member_type.lower() == "faculty" for m in members
    )
    active_count = sum(
        m.status.lower() == "active" for m in members
    )
    suspended_count = sum(
        m.status.lower() == "suspended" for m in members
    )

    # ==========================================
    # SUMMARY CARDS
    # ==========================================

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Members", total_members)
    c2.metric("Students", student_count)
    c3.metric("Faculty", faculty_count)
    c4.metric("Active", active_count)
    c5.metric("Suspended", suspended_count)

    st.divider()

    # ==========================================
    # TABS
    # ==========================================

    (
        directory_tab,
        register_tab,
        details_tab,
        edit_tab,
        status_tab
    ) = st.tabs([
        "👥 Member Directory",
        "➕ Register Member",
        "🔍 Member Details",
        "✏️ Edit Member",
        "🔐 Account Status"
    ])

    # Shared searchable member options
    member_options = {
        f"{m.member_id} — {m.name}": m.member_id
        for m in members
    }

    # ==========================================
    # TAB 1: MEMBER DIRECTORY
    # ==========================================

    with directory_tab:

        st.subheader("Member Directory")

        search_col, type_col, status_col = st.columns([2, 1, 1])

        with search_col:
            search_query = st.text_input(
                "Search Members",
                placeholder="Search by ID, name or email...",
                key="member_search"
            )

        with type_col:
            selected_type = st.selectbox(
                "Member Type",
                ["All Types", "Student", "Faculty"],
                key="member_type_filter"
            )

        with status_col:
            selected_status = st.selectbox(
                "Account Status",
                ["All Statuses", "Active", "Suspended"],
                key="member_status_filter"
            )

        filtered_members = members

        if search_query.strip():
            query = search_query.strip().lower()
            filtered_members = [
                m for m in filtered_members
                if query in m.member_id.lower()
                or query in m.name.lower()
                or query in m.email.lower()
            ]

        if selected_type != "All Types":
            filtered_members = [
                m for m in filtered_members
                if m.member_type.lower() == selected_type.lower()
            ]

        if selected_status != "All Statuses":
            filtered_members = [
                m for m in filtered_members
                if m.status.lower() == selected_status.lower()
            ]

        st.caption(
            f"Showing {len(filtered_members)} of {len(members)} members"
        )

        records = [
            {
                "Member ID": m.member_id,
                "Name": m.name,
                "Type": m.member_type,
                "Email": m.email,
                "Phone": m.phone,
                "Join Date": str(m.join_date),
                "Status": m.status
            }
            for m in filtered_members
        ]

        if records:
            st.dataframe(
                pd.DataFrame(records),
                width="stretch",
                hide_index=True,
                height=450
            )
        else:
            st.info("No members match your filters.")

    # ==========================================
    # TAB 2: REGISTER MEMBER
    # ==========================================

    with register_tab:

        st.subheader("Register New Member")

        member_type = st.radio(
            "Member Type",
            ["Student", "Faculty"],
            horizontal=True,
            key="register_member_type"
        )

        prefix = "S" if member_type == "Student" else "F"

        existing_numbers = [
            int(m.member_id[1:])
            for m in members
            if m.member_id.startswith(prefix)
            and m.member_id[1:].isdigit()
        ]

        next_number = max(existing_numbers, default=0) + 1
        new_member_id = f"{prefix}{next_number:03d}"

        st.info(f"New Member ID: {new_member_id}")

        with st.form("register_member_form", clear_on_submit=True):

            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")

            submitted = st.form_submit_button(
                "➕ Register Member",
                type="primary",
                width="stretch"
            )

        if submitted:

            if not name.strip() or not email.strip() or not phone.strip():
                st.error("Please complete all fields.")

            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")

            else:
                member_class = (
                    StudentMember
                    if member_type == "Student"
                    else FacultyMember
                )

                # Assumes constructor:
                # (member_id, name, email, phone, join_date)
                new_member = member_class(
                    new_member_id,
                    name.strip(),
                    email.strip(),
                    phone.strip()
                )

                if library.register_member(new_member):
                    st.success(
                        f"{member_type} {new_member_id} registered successfully!"
                    )
                else:
                    st.error(
                        "Registration failed. Check for duplicate member details."
                    )

    # ==========================================
    # TAB 3: MEMBER DETAILS
    # ==========================================

    with details_tab:

        st.subheader("Member Details")

        if not members:
            st.info("No registered members.")

        else:
            selected_member = st.selectbox(
                "Select Member",
                options=list(member_options.keys()),
                index=None,
                placeholder="Search by member ID or name...",
                key="member_details_selection"
            )

            if selected_member:

                member_id = member_options[selected_member]
                member = library.get_member(member_id)

                if member is None:
                    st.error("Member not found.")

                else:
                    st.divider()
                    st.markdown(f"### 👤 {member.name}")
                    st.caption(f"Member ID: {member.member_id}")

                    info1, info2 = st.columns(2)

                    with info1:
                        st.write(f"**Type:** {member.member_type}")
                        st.write(f"**Email:** {member.email}")
                        st.write(f"**Phone:** {member.phone}")

                    with info2:
                        st.write(f"**Joined:** {member.join_date}")
                        st.write(f"**Status:** {member.status}")

                    st.divider()
                    st.subheader("Borrowing History")

                    member_loans = library.get_member_loans(member_id)

                    if member_loans:

                        active_loans = sum(
                            loan.status.lower() == "active"
                            for loan in member_loans
                        )

                        returned_loans = sum(
                            loan.status.lower() == "returned"
                            for loan in member_loans
                        )

                        overdue_loans = sum(
                            loan.status.lower() == "active"
                            and date.fromisoformat(str(loan.due_date)) < date.today()
                            for loan in member_loans
                        )

                        lc1, lc2, lc3, lc4 = st.columns(4)

                        lc1.metric("Total Loans", len(member_loans))
                        lc2.metric("Active Loans", active_loans)
                        lc3.metric("Returned", returned_loans)
                        lc4.metric("Overdue", overdue_loans)

                        loan_records = []

                        for loan in member_loans:
                            book = library.get_book(loan.book_id)

                            loan_records.append({
                                "Loan ID": loan.loan_id,
                                "Book": (
                                    book.title if book else loan.book_id
                                ),
                                "Borrow Date": str(loan.borrow_date),
                                "Due Date": str(loan.due_date),
                                "Return Date": (
                                    str(loan.return_date)
                                    if loan.return_date
                                    else "—"
                                ),
                                "Status": loan.status
                            })

                        st.dataframe(
                            pd.DataFrame(loan_records),
                            width="stretch",
                            hide_index=True
                        )

                    else:
                        st.info(
                            "This member has no borrowing history."
                        )

    # ==========================================
    # TAB 4: EDIT MEMBER
    # ==========================================

    with edit_tab:

        st.subheader("Update Member Information")

        if not members:
            st.info("No members available to edit.")

        else:
            selected_member = st.selectbox(
                "Select Member to Edit",
                options=list(member_options.keys()),
                index=None,
                placeholder="Search by member ID or name...",
                key="edit_member_selection"
            )

            if selected_member:

                member_id = member_options[selected_member]
                member = library.get_member(member_id)

                if member is None:
                    st.error("Member not found.")

                else:
                    st.info(f"Editing Member ID: {member.member_id}")

                    with st.form(f"edit_member_form_{member_id}"):

                        new_name = st.text_input(
                            "Full Name",
                            value=member.name
                        )

                        new_email = st.text_input(
                            "Email Address",
                            value=member.email
                        )

                        new_phone = st.text_input(
                            "Phone Number",
                            value=member.phone
                        )

                        submitted = st.form_submit_button(
                            "💾 Save Changes",
                            type="primary",
                            width="stretch"
                        )

                    if submitted:

                        if not all([
                            new_name.strip(),
                            new_email.strip(),
                            new_phone.strip()
                        ]):
                            st.error("All fields are required.")

                        elif (
                            "@" not in new_email
                            or "." not in new_email.split("@")[-1]
                        ):
                            st.error("Please enter a valid email address.")

                        else:
                            updates = {}

                            if new_name.strip() != member.name:
                                updates["name"] = new_name.strip()

                            if new_email.strip() != member.email:
                                updates["email"] = new_email.strip()

                            if new_phone.strip() != member.phone:
                                updates["phone"] = new_phone.strip()

                            if not updates:
                                st.info("No changes were made.")

                            elif library.update_member(
                                member_id, **updates
                            ):
                                st.success(
                                    f"Member {member_id} updated successfully!"
                                )
                            else:
                                st.error(
                                    "Unable to update member information."
                                )

    # ==========================================
    # TAB 5: SUSPEND / ACTIVATE MEMBER
    # ==========================================

    with status_tab:

        st.subheader("Manage Account Status")
        st.caption(
            "Suspend or reactivate a library membership."
        )

        if not members:
            st.info("No members available.")

        else:
            selected_member = st.selectbox(
                "Select Member",
                options=list(member_options.keys()),
                index=None,
                placeholder="Search by member ID or name...",
                key="status_member_selection"
            )

            if selected_member:

                member_id = member_options[selected_member]
                member = library.get_member(member_id)

                if member is None:
                    st.error("Member not found.")

                else:
                    st.divider()

                    st.markdown(f"### 👤 {member.name}")
                    st.write(f"**Member ID:** {member.member_id}")
                    st.write(f"**Member Type:** {member.member_type}")
                    st.write(f"**Email:** {member.email}")

                    current_status = member.status.lower()

                    if current_status == "active":

                        st.success("Current Status: Active")

                        st.warning(
                            "Suspending this member will prevent "
                            "them from borrowing new books."
                        )

                        with st.form(
                            f"suspend_member_form_{member_id}"
                        ):

                            confirmed = st.checkbox(
                                "I confirm that I want to suspend "
                                "this member."
                            )

                            submitted = st.form_submit_button(
                                "🔒 Suspend Member",
                                type="primary",
                                width="stretch"
                            )

                        if submitted:

                            if not confirmed:
                                st.error(
                                    "Please confirm the suspension."
                                )

                            elif library.suspend_member(member_id):
                                st.success(
                                    f"Member {member_id} suspended successfully!"
                                )

                            else:
                                st.error(
                                    "Unable to suspend this member."
                                )

                    elif current_status == "suspended":

                        st.error("Current Status: Suspended")

                        st.info(
                            "Activating this member will restore "
                            "their borrowing privileges."
                        )

                        if st.button(
                            "🔓 Activate Member",
                            type="primary",
                            width="stretch",
                            key=f"activate_member_{member_id}"
                        ):

                            if library.activate_member(member_id):
                                st.success(
                                    f"Member {member_id} activated successfully!"
                                )

                            else:
                                st.error(
                                    "Unable to activate this member."
                                )

                    else:
                        st.warning(
                            f"Unrecognized account status: {member.status}"
                        )


elif page == "Loan Management":

    st.title("📖 Loan Management")
    st.caption(
        "Issue books, process returns, monitor active loans, "
        "and track overdue books and fines."
    )

    # ==========================================
    # LOAD DATA
    # ==========================================

    books = library.list_books()
    members = library.list_members()
    loans = list(library.loans.values())

    today = date.today()

    def loan_date(value):
        if value is None or value == "":
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(str(value)[:10])
        except (ValueError, TypeError):
            return None

    def is_active(loan):
        return str(loan.status).lower() == "active"

    def is_overdue(loan):
        due = loan_date(loan.due_date)
        return (
            is_active(loan)
            and due is not None
            and due < today
        )

    def get_fine(loan):
        try:
            return max(0, float(loan.calculate_fine()))
        except (TypeError, ValueError, AttributeError):
            return 0.0

    def book_label(book_id):
        book = library.get_book(book_id)
        return book.title if book else f"Unknown Book ({book_id})"

    def member_label(member_id):
        member = library.get_member(member_id)
        return member.name if member else f"Unknown Member ({member_id})"

    def loan_record(loan):
        due = loan_date(loan.due_date)
        overdue = is_overdue(loan)

        return {
            "Loan ID": loan.loan_id,
            "Book ID": loan.book_id,
            "Book Title": book_label(loan.book_id),
            "Member ID": loan.member_id,
            "Member Name": member_label(loan.member_id),
            "Borrow Date": str(loan.borrow_date),
            "Due Date": str(loan.due_date),
            "Return Date": (
                str(loan.return_date)
                if loan.return_date
                else "—"
            ),
            "Status": (
                "Overdue" if overdue else str(loan.status).title()
            ),
            "Days Overdue": (
                (today - due).days if overdue else 0
            ),
            "Fine (BDT)": round(get_fine(loan), 2)
        }

    active_loans = [loan for loan in loans if is_active(loan)]
    returned_loans = [loan for loan in loans if not is_active(loan)]
    overdue_loans = [loan for loan in loans if is_overdue(loan)]

    total_fines = sum(get_fine(loan) for loan in overdue_loans)

    # ==========================================
    # SUMMARY CARDS
    # ==========================================

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Loans", len(loans))
    c2.metric("Active Loans", len(active_loans))
    c3.metric("Returned", len(returned_loans))
    c4.metric("Overdue", len(overdue_loans))
    c5.metric("Current Overdue Fines", f"৳{total_fines:,.2f}")

    st.divider()

    # ==========================================
    # TABS
    # ==========================================

    (
        directory_tab,
        borrow_tab,
        return_tab,
        active_tab,
        overdue_tab,
        details_tab
    ) = st.tabs([
        "📋 Loan Directory",
        "📚 Borrow Book",
        "↩️ Return Book",
        "📖 Active Loans",
        "⚠️ Overdue Loans",
        "🔍 Loan Details"
    ])

    # ==========================================
    # TAB 1: LOAN DIRECTORY
    # ==========================================

    with directory_tab:

        st.subheader("Loan Directory")
        st.caption("Browse and filter all borrowing records.")

        search_col, status_col = st.columns([3, 1])

        with search_col:
            search_query = st.text_input(
                "Search Loans",
                placeholder="Loan ID, book, member or name...",
                key="loan_directory_search"
            )

        with status_col:
            selected_status = st.selectbox(
                "Loan Status",
                ["All Loans", "Active", "Returned", "Overdue"],
                key="loan_directory_status"
            )

        filtered_loans = loans

        if search_query.strip():
            query = search_query.strip().lower()

            filtered_loans = [
                loan for loan in filtered_loans
                if query in str(loan.loan_id).lower()
                or query in str(loan.book_id).lower()
                or query in str(loan.member_id).lower()
                or query in book_label(loan.book_id).lower()
                or query in member_label(loan.member_id).lower()
            ]

        if selected_status == "Active":
            filtered_loans = [
                loan for loan in filtered_loans
                if is_active(loan)
            ]

        elif selected_status == "Returned":
            filtered_loans = [
                loan for loan in filtered_loans
                if not is_active(loan)
            ]

        elif selected_status == "Overdue":
            filtered_loans = [
                loan for loan in filtered_loans
                if is_overdue(loan)
            ]

        st.caption(
            f"Showing {len(filtered_loans)} of {len(loans)} loans"
        )

        if filtered_loans:
            st.dataframe(
                pd.DataFrame([
                    loan_record(loan)
                    for loan in filtered_loans
                ]),
                width="stretch",
                hide_index=True,
                height=480
            )
        else:
            st.info("No loan records match your filters.")

    # ==========================================
    # TAB 2: BORROW BOOK
    # ==========================================

    with borrow_tab:

        st.subheader("Issue a Book")
        st.caption(
            "Select an active member and an available book."
        )

        eligible_members = [
            member for member in members
            if str(member.status).lower() == "active"
        ]

        available_books = [
            book for book in books
            if book.available_copies > 0
        ]

        if not eligible_members:
            st.warning("No active members are available.")

        elif not available_books:
            st.warning("No books are currently available.")

        else:
            member_options = {
                f"{m.member_id} — {m.name} ({m.member_type})":
                    m.member_id
                for m in eligible_members
            }

            book_options = {
                f"{b.book_id} — {b.title} "
                f"({b.available_copies} available)":
                    b.book_id
                for b in available_books
            }

            with st.form("issue_book_form"):

                selected_member = st.selectbox(
                    "Select Member",
                    list(member_options.keys()),
                    index=None,
                    placeholder="Search member ID or name..."
                )

                selected_book = st.selectbox(
                    "Select Book",
                    list(book_options.keys()),
                    index=None,
                    placeholder="Search book ID or title..."
                )

                submitted = st.form_submit_button(
                    "📚 Issue Book",
                    type="primary",
                    width="stretch"
                )

            if submitted:

                if not selected_member or not selected_book:
                    st.error(
                        "Please select both a member and a book."
                    )

                else:
                    member_id = member_options[selected_member]
                    book_id = book_options[selected_book]

                    try:
                        # Assumes borrow_book(book_id, member_id)
                        result = library.borrow_book(
                            member_id,book_id, 
                        )

                        if result is False or result is None:
                            st.error(
                                "Borrowing failed. Check membership "
                                "eligibility and borrowing limits."
                            )
                        else:
                            st.session_state["loan_notice"] = (
                                f"Book {book_id} issued successfully "
                                f"to member {member_id}."
                            )
                            st.rerun()

                    except (ValueError, TypeError) as exc:
                        st.error(f"Unable to issue book: {exc}")

    # ==========================================
    # TAB 3: RETURN BOOK
    # ==========================================

    with return_tab:

        st.subheader("Process Book Return")
        st.caption(
            "Select an active loan and process the return."
        )

        if not active_loans:
            st.info("There are no active loans to return.")

        else:
            return_options = {
                (
                    f"{loan.loan_id} — "
                    f"{book_label(loan.book_id)} — "
                    f"{member_label(loan.member_id)}"
                ): loan.loan_id
                for loan in active_loans
            }

            selected_return = st.selectbox(
                "Select Active Loan",
                list(return_options.keys()),
                index=None,
                placeholder="Search loan ID, book or member...",
                key="return_loan_selection"
            )

            if selected_return:

                loan_id = return_options[selected_return]
                loan = library.get_loan(loan_id)

                if loan is None:
                    st.error("Loan not found.")

                else:
                    st.divider()

                    st.markdown(
                        f"### 📖 {book_label(loan.book_id)}"
                    )
                    st.write(f"**Loan ID:** {loan.loan_id}")
                    st.write(
                        f"**Member:** {member_label(loan.member_id)}"
                    )
                    st.write(f"**Borrowed:** {loan.borrow_date}")
                    st.write(f"**Due Date:** {loan.due_date}")

                    fine = get_fine(loan)

                    if is_overdue(loan):
                        st.warning(
                            f"This loan is overdue. "
                            f"Calculated fine: ৳{fine:,.2f}"
                        )
                    else:
                        st.success("This loan is not overdue.")

                    with st.form(
                        f"return_loan_form_{loan_id}"
                    ):

                        confirmed = st.checkbox(
                            "Confirm that the book has been returned."
                        )

                        submitted = st.form_submit_button(
                            "↩️ Process Return",
                            type="primary",
                            width="stretch"
                        )

                    if submitted:

                        if not confirmed:
                            st.error("Please confirm the return.")

                        else:
                            try:
                                # Assumes return_book(loan_id)
                                result = library.return_book(loan_id)

                                if result is False or result is None:
                                    st.error(
                                        "Unable to process this return."
                                    )
                                else:
                                    st.session_state["loan_notice"] = (
                                        f"Loan {loan_id} returned "
                                        "successfully."
                                    )
                                    st.rerun()

                            except (ValueError, TypeError) as exc:
                                st.error(
                                    f"Unable to process return: {exc}"
                                )

    # ==========================================
    # TAB 4: ACTIVE LOANS
    # ==========================================

    with active_tab:

        st.subheader("Active Loans")
        st.caption("Books currently checked out by members.")

        if active_loans:

            st.metric(
                "Currently Borrowed Books",
                len(active_loans)
            )

            st.dataframe(
                pd.DataFrame([
                    loan_record(loan)
                    for loan in active_loans
                ]),
                width="stretch",
                hide_index=True,
                height=450
            )

        else:
            st.success("There are no active loans.")

    # ==========================================
    # TAB 5: OVERDUE LOANS
    # ==========================================

    with overdue_tab:

        st.subheader("Overdue Loans")
        st.caption(
            "Monitor late returns and outstanding overdue fines."
        )

        if overdue_loans:

            overdue_c1, overdue_c2 = st.columns(2)

            overdue_c1.metric(
                "Overdue Loans",
                len(overdue_loans)
            )

            overdue_c2.metric(
                "Current Overdue Fines",
                f"৳{total_fines:,.2f}"
            )

            overdue_records = [
                loan_record(loan)
                for loan in overdue_loans
            ]

            overdue_records.sort(
                key=lambda record: record["Days Overdue"],
                reverse=True
            )

            st.dataframe(
                pd.DataFrame(overdue_records),
                width="stretch",
                hide_index=True,
                height=450
            )

        else:
            st.success("No overdue loans. All active loans are on time!")

    # ==========================================
    # TAB 6: LOAN DETAILS
    # ==========================================

    with details_tab:

        st.subheader("Loan Details")
        st.caption("Review an individual borrowing transaction.")

        if not loans:
            st.info("No loans have been recorded.")

        else:
            loan_options = {
                (
                    f"{loan.loan_id} — "
                    f"{book_label(loan.book_id)} — "
                    f"{member_label(loan.member_id)}"
                ): loan.loan_id
                for loan in loans
            }

            selected_loan = st.selectbox(
                "Select Loan",
                list(loan_options.keys()),
                index=None,
                placeholder="Search loan ID, book or member...",
                key="loan_details_selection"
            )

            if selected_loan:

                loan_id = loan_options[selected_loan]
                loan = library.get_loan(loan_id)

                if loan is None:
                    st.error("Loan not found.")

                else:
                    st.divider()

                    st.markdown(
                        f"### 📖 {book_label(loan.book_id)}"
                    )
                    st.caption(f"Loan ID: {loan.loan_id}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(
                            f"**Book ID:** {loan.book_id}"
                        )
                        st.write(
                            f"**Member ID:** {loan.member_id}"
                        )
                        st.write(
                            f"**Member:** "
                            f"{member_label(loan.member_id)}"
                        )

                    with col2:
                        st.write(
                            f"**Borrow Date:** {loan.borrow_date}"
                        )
                        st.write(
                            f"**Due Date:** {loan.due_date}"
                        )
                        st.write(
                            f"**Return Date:** "
                            f"{loan.return_date or 'Not returned'}"
                        )

                    st.divider()

                    status_col, fine_col = st.columns(2)

                    with status_col:
                        if is_overdue(loan):
                            st.error("Status: Overdue")
                        elif is_active(loan):
                            st.info("Status: Active")
                        else:
                            st.success("Status: Returned")

                    with fine_col:
                        st.metric(
                            "Calculated Fine",
                            f"৳{get_fine(loan):,.2f}"
                        )

                    due = loan_date(loan.due_date)

                    if is_overdue(loan) and due:
                        st.warning(
                            f"This loan is "
                            f"{(today - due).days} day(s) overdue."
                        )

    # ==========================================
    # SUCCESS NOTIFICATION
    # ==========================================

    if "loan_notice" in st.session_state:
        st.toast(
            st.session_state.pop("loan_notice"),
            icon="✅"
        )



elif page == "Reports & Analytics":

    st.title("📊 Reports & Analytics")
    st.caption(
        "Explore library performance, borrowing patterns, "
        "member activity, inventory, and outstanding fines."
    )

    # ==========================================
    # LOAD DATA
    # ==========================================

    books = library.list_books()
    members = library.list_members()
    loans = list(library.loans.values())

    today = date.today()

    def report_date(value):
        if value is None or value == "":
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        try:
            return date.fromisoformat(str(value)[:10])
        except (TypeError, ValueError):
            return None

    def loan_is_active(loan):
        return str(loan.status).lower() == "active"

    def loan_is_overdue(loan):
        due = report_date(loan.due_date)
        return (
            loan_is_active(loan)
            and due is not None
            and due < today
        )

    def loan_fine(loan):
        try:
            return max(0.0, float(loan.calculate_fine()))
        except (TypeError, ValueError, AttributeError):
            return 0.0

    def book_name(book_id):
        book = library.get_book(book_id)
        return book.title if book else f"Unknown ({book_id})"

    def member_name(member_id):
        member = library.get_member(member_id)
        return member.name if member else f"Unknown ({member_id})"

    # ==========================================
    # PREPARE DATAFRAMES
    # ==========================================

    book_rows = [
        {
            "Book ID": b.book_id,
            "Title": b.title,
            "Author": b.author,
            "Category": b.category,
            "Total Copies": b.total_copies,
            "Available Copies": b.available_copies,
            "Borrowed Copies": (
                b.total_copies - b.available_copies
            )
        }
        for b in books
    ]

    member_rows = [
        {
            "Member ID": m.member_id,
            "Name": m.name,
            "Member Type": m.member_type,
            "Email": m.email,
            "Phone": m.phone,
            "Join Date": str(m.join_date),
            "Status": m.status
        }
        for m in members
    ]

    loan_rows = []

    for loan in loans:
        due = report_date(loan.due_date)
        borrowed = report_date(loan.borrow_date)
        overdue = loan_is_overdue(loan)

        loan_rows.append({
            "Loan ID": loan.loan_id,
            "Book ID": loan.book_id,
            "Book Title": book_name(loan.book_id),
            "Member ID": loan.member_id,
            "Member Name": member_name(loan.member_id),
            "Borrow Date": borrowed,
            "Due Date": due,
            "Return Date": report_date(loan.return_date),
            "Status": (
                "Overdue" if overdue
                else str(loan.status).title()
            ),
            "Days Overdue": (
                (today - due).days if overdue else 0
            ),
            "Fine (BDT)": round(loan_fine(loan), 2)
        })

    books_df = pd.DataFrame(book_rows)
    members_df = pd.DataFrame(member_rows)
    loans_df = pd.DataFrame(loan_rows)

    # ==========================================
    # SUMMARY METRICS
    # ==========================================

    total_titles = len(books)
    total_copies = sum(b.total_copies for b in books)
    available_copies = sum(b.available_copies for b in books)

    active_loans = [
        loan for loan in loans if loan_is_active(loan)
    ]
    returned_loans = [
        loan for loan in loans if not loan_is_active(loan)
    ]
    overdue_loans = [
        loan for loan in loans if loan_is_overdue(loan)
    ]

    outstanding_fines = sum(
        loan_fine(loan) for loan in active_loans
    )

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("Book Titles", f"{total_titles:,}")
    m2.metric("Total Copies", f"{total_copies:,}")
    m3.metric("Members", f"{len(members):,}")
    m4.metric("Total Loans", f"{len(loans):,}")
    m5.metric("Outstanding Fines", f"৳{outstanding_fines:,.2f}")

    st.divider()

    # ==========================================
    # REPORT TABS
    # ==========================================

    (
        overview_tab,
        books_tab,
        members_tab,
        loans_tab,
        fines_tab,
        export_tab
    ) = st.tabs([
        "📈 Overview",
        "📚 Book Analytics",
        "👥 Member Analytics",
        "📖 Loan Analytics",
        "💰 Fine Analytics",
        "📥 Export Reports"
    ])

    # ==========================================
    # TAB 1: LIBRARY OVERVIEW
    # ==========================================

    with overview_tab:

        st.subheader("Library Performance Overview")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Active Loans", len(active_loans))
        c2.metric("Returned Loans", len(returned_loans))
        c3.metric("Overdue Loans", len(overdue_loans))

        availability_rate = (
            available_copies / total_copies * 100
            if total_copies else 0
        )
        c4.metric("Inventory Availability", f"{availability_rate:.1f}%")

        left, right = st.columns(2)

        with left:
            st.markdown("#### Inventory Availability")

            fig = px.pie(
                names=["Available", "Borrowed"],
                values=[
                    available_copies,
                    total_copies - available_copies
                ],
                hole=0.6,
                color_discrete_sequence=[
                    "#22c55e", "#ef4444"
                ]
            )

            fig.update_layout(
                template="plotly_dark",
                height=360,
                margin=dict(l=10, r=10, t=20, b=10),
                showlegend=True
            )

            st.plotly_chart(fig, width="stretch")

        with right:
            st.markdown("#### Loan Status Distribution")

            status_counts = {
                "Active": len(active_loans) - len(overdue_loans),
                "Overdue": len(overdue_loans),
                "Returned": len(returned_loans)
            }

            fig = px.bar(
                x=list(status_counts.keys()),
                y=list(status_counts.values()),
                color=list(status_counts.keys()),
                color_discrete_map={
                    "Active": "#3b82f6",
                    "Overdue": "#ef4444",
                    "Returned": "#22c55e"
                },
                labels={"x": "Status", "y": "Loans"}
            )

            fig.update_layout(
                template="plotly_dark",
                height=360,
                showlegend=False,
                margin=dict(l=10, r=10, t=20, b=10)
            )

            st.plotly_chart(fig, width="stretch")

    # ==========================================
    # TAB 2: BOOK ANALYTICS
    # ==========================================

    with books_tab:

        st.subheader("Book Collection Analytics")

        if books_df.empty:
            st.info("No book data available.")

        else:
            left, right = st.columns(2)

            with left:
                st.markdown("#### Books by Category")

                category_counts = (
                    books_df.groupby("Category")
                    .size()
                    .reset_index(name="Titles")
                    .sort_values("Titles", ascending=False)
                )

                fig = px.bar(
                    category_counts,
                    x="Category",
                    y="Titles",
                    color="Titles",
                    color_continuous_scale="Reds"
                )

                fig.update_layout(
                    template="plotly_dark",
                    height=390,
                    showlegend=False
                )

                st.plotly_chart(fig, width="stretch")

            with right:
                st.markdown("#### Copies by Category")

                category_copies = (
                    books_df.groupby("Category")[
                        ["Available Copies", "Borrowed Copies"]
                    ]
                    .sum()
                    .reset_index()
                )

                fig = px.bar(
                    category_copies,
                    x="Category",
                    y=["Available Copies", "Borrowed Copies"],
                    barmode="stack",
                    color_discrete_sequence=[
                        "#22c55e", "#ef4444"
                    ]
                )

                fig.update_layout(
                    template="plotly_dark",
                    height=390,
                    legend_title_text="Copy Status"
                )

                st.plotly_chart(fig, width="stretch")

            st.divider()
            st.markdown("#### Most Borrowed Books")

            borrow_counts = {}

            for loan in loans:
                borrow_counts[loan.book_id] = (
                    borrow_counts.get(loan.book_id, 0) + 1
                )

            top_books = sorted(
                borrow_counts.items(),
                key=lambda item: item[1],
                reverse=True
            )[:10]

            if top_books:
                top_df = pd.DataFrame([
                    {
                        "Book ID": book_id,
                        "Title": book_name(book_id),
                        "Times Borrowed": count
                    }
                    for book_id, count in top_books
                ])

                fig = px.bar(
                    top_df.sort_values("Times Borrowed"),
                    x="Times Borrowed",
                    y="Title",
                    orientation="h",
                    color="Times Borrowed",
                    color_continuous_scale="Reds"
                )

                fig.update_layout(
                    template="plotly_dark",
                    height=450,
                    showlegend=False
                )

                st.plotly_chart(fig, width="stretch")

                st.dataframe(
                    top_df,
                    width="stretch",
                    hide_index=True
                )
            else:
                st.info("No borrowing history available.")

    # ==========================================
    # TAB 3: MEMBER ANALYTICS
    # ==========================================

    with members_tab:

        st.subheader("Member Analytics")

        if members_df.empty:
            st.info("No member data available.")

        else:
            left, right = st.columns(2)

            with left:
                st.markdown("#### Member Distribution")

                type_counts = (
                    members_df["Member Type"]
                    .value_counts()
                    .reset_index()
                )

                type_counts.columns = ["Type", "Members"]

                fig = px.pie(
                    type_counts,
                    names="Type",
                    values="Members",
                    hole=0.55,
                    color_discrete_sequence=[
                        "#ef4444", "#3b82f6"
                    ]
                )

                fig.update_layout(
                    template="plotly_dark",
                    height=370
                )

                st.plotly_chart(fig, width="stretch")

            with right:
                st.markdown("#### Membership Status")

                status_counts = (
                    members_df["Status"]
                    .value_counts()
                    .reset_index()
                )

                status_counts.columns = ["Status", "Members"]

                fig = px.bar(
                    status_counts,
                    x="Status",
                    y="Members",
                    color="Status",
                    color_discrete_map={
                        "Active": "#22c55e",
                        "Suspended": "#ef4444"
                    }
                )

                fig.update_layout(
                    template="plotly_dark",
                    height=370,
                    showlegend=False
                )

                st.plotly_chart(fig, width="stretch")

            st.divider()
            st.markdown("#### Most Active Borrowers")

            member_borrows = {}

            for loan in loans:
                member_borrows[loan.member_id] = (
                    member_borrows.get(loan.member_id, 0) + 1
                )

            top_members = sorted(
                member_borrows.items(),
                key=lambda item: item[1],
                reverse=True
            )[:10]

            if top_members:
                top_members_df = pd.DataFrame([
                    {
                        "Member ID": member_id,
                        "Name": member_name(member_id),
                        "Total Borrowings": count
                    }
                    for member_id, count in top_members
                ])

                fig = px.bar(
                    top_members_df.sort_values("Total Borrowings"),
                    x="Total Borrowings",
                    y="Name",
                    orientation="h",
                    color="Total Borrowings",
                    color_continuous_scale="Reds"
                )

                fig.update_layout(
                    template="plotly_dark",
                    height=430,
                    showlegend=False
                )

                st.plotly_chart(fig, width="stretch")

                st.dataframe(
                    top_members_df,
                    width="stretch",
                    hide_index=True
                )

            else:
                st.info("No member borrowing activity recorded.")

    # ==========================================
    # TAB 4: LOAN ANALYTICS
    # ==========================================

    with loans_tab:

        st.subheader("Borrowing & Loan Analytics")

        if loans_df.empty:
            st.info("No loan data available.")

        else:
            trend_df = loans_df.copy()

            trend_df["Borrow Date"] = pd.to_datetime(
                trend_df["Borrow Date"],
                errors="coerce"
            )

            trend_df = trend_df.dropna(
                subset=["Borrow Date"]
            )

            st.markdown("#### Monthly Borrowing Trend")

            if not trend_df.empty:

                trend_df["Month"] = (
                    trend_df["Borrow Date"]
                    .dt.to_period("M")
                    .astype(str)
                )

                monthly = (
                    trend_df.groupby("Month")
                    .size()
                    .reset_index(name="Loans")
                    .sort_values("Month")
                )

                fig = px.area(
                    monthly,
                    x="Month",
                    y="Loans",
                    markers=True
                )

                fig.update_traces(
                    line_color="#ef4444",
                    fillcolor="rgba(239,68,68,0.18)"
                )

                fig.update_layout(
                    template="plotly_dark",
                    height=390
                )

                st.plotly_chart(fig, width="stretch")

            st.divider()
            st.markdown("#### Loan Activity by Member Type")

            member_type_lookup = {
                m.member_id: m.member_type
                for m in members
            }

            type_activity = {}

            for loan in loans:
                member_type = member_type_lookup.get(
                    loan.member_id, "Unknown"
                )

                type_activity[member_type] = (
                    type_activity.get(member_type, 0) + 1
                )

            activity_df = pd.DataFrame([
                {
                    "Member Type": member_type,
                    "Loans": count
                }
                for member_type, count in type_activity.items()
            ])

            if not activity_df.empty:
                fig = px.bar(
                    activity_df,
                    x="Member Type",
                    y="Loans",
                    color="Member Type"
                )

                fig.update_layout(
                    template="plotly_dark",
                    height=350,
                    showlegend=False
                )

                st.plotly_chart(fig, width="stretch")

            st.divider()
            st.markdown("#### Recent Loan Records")

            recent_df = loans_df.copy()

            recent_df["Sort Date"] = pd.to_datetime(
                recent_df["Borrow Date"],
                errors="coerce"
            )

            recent_df = (
                recent_df.sort_values(
                    "Sort Date", ascending=False
                )
                .drop(columns=["Sort Date"])
                .head(15)
            )

            st.dataframe(
                recent_df,
                width="stretch",
                hide_index=True
            )

    # ==========================================
    # TAB 5: FINE ANALYTICS
    # ==========================================

    with fines_tab:

        st.subheader("Fine Analytics")
        st.caption(
            "Calculated outstanding fines on active loans. "
            "Historical paid amounts are not tracked here."
        )

        fine_loans = [
            loan for loan in active_loans
            if loan_fine(loan) > 0
        ]

        f1, f2, f3 = st.columns(3)

        f1.metric(
            "Outstanding Fines",
            f"৳{outstanding_fines:,.2f}"
        )
        f2.metric(
            "Loans With Fines",
            len(fine_loans)
        )
        f3.metric(
            "Average Fine",
            f"৳{outstanding_fines / len(fine_loans):,.2f}"
            if fine_loans else "৳0.00"
        )

        if fine_loans:

            st.divider()
            st.markdown("#### Outstanding Fines by Member")

            member_fines = {}

            for loan in fine_loans:
                member_fines[loan.member_id] = (
                    member_fines.get(loan.member_id, 0)
                    + loan_fine(loan)
                )

            fine_df = pd.DataFrame([
                {
                    "Member ID": member_id,
                    "Member Name": member_name(member_id),
                    "Outstanding Fine (BDT)": round(amount, 2)
                }
                for member_id, amount in member_fines.items()
            ])

            fine_df = fine_df.sort_values(
                "Outstanding Fine (BDT)",
                ascending=False
            )

            fig = px.bar(
                fine_df.head(10).sort_values(
                    "Outstanding Fine (BDT)"
                ),
                x="Outstanding Fine (BDT)",
                y="Member Name",
                orientation="h",
                color="Outstanding Fine (BDT)",
                color_continuous_scale="Reds"
            )

            fig.update_layout(
                template="plotly_dark",
                height=420,
                showlegend=False
            )

            st.plotly_chart(fig, width="stretch")

            st.dataframe(
                fine_df,
                width="stretch",
                hide_index=True
            )

        else:
            st.success("There are currently no outstanding fines.")

    # ==========================================
    # TAB 6: EXPORT REPORTS
    # ==========================================

    with export_tab:

        st.subheader("Export Library Reports")
        st.caption(
            "Download the current library data as CSV files."
        )

        def csv_bytes(df):
            return df.to_csv(index=False).encode("utf-8-sig")

        export_date = today.isoformat()

        st.markdown("#### Book Inventory Report")
        st.write(
            f"Contains {len(books_df)} book titles, "
            "categories, authors, and copy counts."
        )

        st.download_button(
            "📥 Download Books CSV",
            data=csv_bytes(books_df),
            file_name=f"library_books_{export_date}.csv",
            mime="text/csv",
            disabled=books_df.empty,
            width="stretch"
        )

        st.divider()

        st.markdown("#### Member Directory Report")
        st.write(
            f"Contains {len(members_df)} members and "
            "their account information."
        )

        st.download_button(
            "📥 Download Members CSV",
            data=csv_bytes(members_df),
            file_name=f"library_members_{export_date}.csv",
            mime="text/csv",
            disabled=members_df.empty,
            width="stretch"
        )

        st.divider()

        st.markdown("#### Loan Transaction Report")
        st.write(
            f"Contains {len(loans_df)} borrowing transactions, "
            "dates, statuses, and calculated fines."
        )

        st.download_button(
            "📥 Download Loans CSV",
            data=csv_bytes(loans_df),
            file_name=f"library_loans_{export_date}.csv",
            mime="text/csv",
            disabled=loans_df.empty,
            width="stretch"
        )

        st.divider()

        st.markdown("#### Overdue Loan Report")

        overdue_export = (
            loans_df[loans_df["Status"] == "Overdue"]
            if not loans_df.empty
            else pd.DataFrame()
        )

        st.write(
            f"Contains {len(overdue_export)} overdue "
            "transactions and their fines."
        )

        st.download_button(
            "📥 Download Overdue Loans CSV",
            data=csv_bytes(overdue_export),
            file_name=f"library_overdue_{export_date}.csv",
            mime="text/csv",
            disabled=overdue_export.empty,
            width="stretch"
        )
