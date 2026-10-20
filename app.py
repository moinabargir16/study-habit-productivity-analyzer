
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# -------------------------------
# 1. Page settings
# -------------------------------

st.set_page_config(
    page_title="Study Habit Analyzer",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Study Habit and Productivity Analyzer")
st.write(
    "Track your study routine, review your progress, "
    "and understand your daily habits."
)

DATA_FILE = "study_data.csv"

COLUMNS = [
    "Date",
    "Study Hours",
    "Sleep Hours",
    "Tasks Planned",
    "Tasks Completed"
]


# -------------------------------
# 2. Load saved records
# -------------------------------

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            data = pd.read_csv(DATA_FILE)
            data["Date"] = pd.to_datetime(
                data["Date"], errors="coerce"
            )
            data = data.dropna(subset=["Date"])

            for column in COLUMNS[1:]:
                data[column] = pd.to_numeric(
                    data[column], errors="coerce"
                )

            data = data.dropna(subset=COLUMNS[1:])
            return data[COLUMNS]

        except (ValueError, OSError, KeyError):
            st.error(
                "The saved data file could not be read. "
                "Check study_data.csv before continuing."
            )

    return pd.DataFrame(columns=COLUMNS)


# -------------------------------
# 3. Daily entry form
# -------------------------------

st.header("Add your daily record")

with st.form("study_form"):
    selected_date = st.date_input("Date")

    study_hours = st.number_input(
        "Hours studied",
        min_value=0.0,
        max_value=24.0,
        value=3.0,
        step=0.5
    )

    sleep_hours = st.number_input(
        "Hours slept",
        min_value=0.0,
        max_value=24.0,
        value=7.0,
        step=0.5
    )

    tasks_planned = st.number_input(
        "Tasks planned",
        min_value=0,
        max_value=100,
        value=5,
        step=1
    )

    tasks_completed = st.number_input(
        "Tasks completed",
        min_value=0,
        max_value=100,
        value=4,
        step=1
    )

    submitted = st.form_submit_button("Save daily record")

    if submitted:
        if tasks_completed > tasks_planned:
            st.error(
                "Tasks completed cannot exceed tasks planned."
            )
        else:
            new_record = pd.DataFrame([{
                "Date": pd.Timestamp(selected_date),
                "Study Hours": study_hours,
                "Sleep Hours": sleep_hours,
                "Tasks Planned": tasks_planned,
                "Tasks Completed": tasks_completed
            }])

            existing_data = load_data()
            updated_data = pd.concat(
                [existing_data, new_record],
                ignore_index=True
            )

            try:
                updated_data.to_csv(DATA_FILE, index=False)
                st.success("Daily record saved successfully!")
                st.rerun()
            except OSError:
                st.error(
                    "The record could not be saved. "
                    "Check the folder permissions."
                )


# -------------------------------
# 4. Display saved records
# -------------------------------

data = load_data()

st.header("Your study records")

if data.empty:
    st.info(
        "No records yet. Enter your first daily record above."
    )

else:
    data = data.sort_values("Date")
    display_data = data.copy()
    display_data["Date"] = (
        display_data["Date"].dt.strftime("%Y-%m-%d")
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------------
    # 5. Calculate statistics
    # -------------------------------

    average_study = np.mean(data["Study Hours"])
    average_sleep = np.mean(data["Sleep Hours"])
    total_tasks = data["Tasks Planned"].sum()
    completed_tasks = data["Tasks Completed"].sum()

    if total_tasks > 0:
        completion_rate = (
            completed_tasks / total_tasks
        ) * 100
    else:
        completion_rate = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average study hours",
        f"{average_study:.1f} hrs"
    )
    col2.metric(
        "Average sleep",
        f"{average_sleep:.1f} hrs"
    )
    col3.metric(
        "Tasks completed",
        f"{int(completed_tasks)}"
    )
    col4.metric(
        "Task completion rate",
        f"{completion_rate:.1f}%"
    )

    # -------------------------------
    # 6. Create charts
    # -------------------------------

    st.header("Visualize your progress")

    chart_data = data.set_index("Date")

    st.subheader("Daily study hours")
    st.line_chart(chart_data["Study Hours"])

    st.subheader("Daily sleep hours")
    st.line_chart(chart_data["Sleep Hours"])

    st.subheader("Tasks planned vs completed")

    task_chart = chart_data[
        ["Tasks Planned", "Tasks Completed"]
    ]
    st.bar_chart(task_chart)

    st.subheader("Study hours and tasks completed")

    fig, ax = plt.subplots()

    ax.scatter(
        data["Study Hours"],
        data["Tasks Completed"]
    )

    ax.set_xlabel("Study hours")
    ax.set_ylabel("Tasks completed")
    ax.set_title("Study Hours vs Tasks Completed")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)

    # -------------------------------
    # 7. Generate simple insights
    # -------------------------------

    st.header("Your productivity insights")

    best_day = data.loc[
        data["Tasks Completed"].idxmax()
    ]

    st.write(
        f"Your highest task count was "
        f"{int(best_day['Tasks Completed'])} tasks "
        f"on {best_day['Date'].strftime('%Y-%m-%d')}."
    )

    if completion_rate >= 80:
        st.success(
            "You completed at least 80% of your planned tasks. "
            "Keep reviewing what works for you."
        )
    else:
        st.info(
            "Try reviewing your daily task list and setting "
            "realistic priorities for the next day."
        )

    if average_study < 2:
        st.info(
            "Your recorded average study time is under "
            "2 hours per day. Consider setting a manageable "
            "study goal that suits your schedule."
        )
    else:
        st.write(
            "Review your study-hour chart to see how your "
            "routine changes from day to day."
        )

    st.caption(
        "These insights describe patterns in your records. "
        "They do not prove that study hours or sleep cause "
        "changes in productivity."
    )
