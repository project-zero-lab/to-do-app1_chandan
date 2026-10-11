import random
import streamlit as st
from datetime import date

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(page_title="My To-Do App", page_icon="✅", layout="centered")

st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.22);
            padding: 12px 14px;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✅ My To-Do App")
st.caption("Manage your daily tasks easily!")

# -------------------------------
# SESSION STATE
# -------------------------------

if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1


# -------------------------------
# TASK OPERATIONS
# -------------------------------

def add_task():
    task = {
        "id": st.session_state.next_id,
        "title": st.session_state.title_input,
        "owner": st.session_state.owner_input,
        "deadline": str(st.session_state.deadline_input),
        "done": st.session_state.status_input,
    }
    st.session_state.tasks.append(task)
    st.session_state.next_id += 1
    st.success("Task added successfully!")


def delete_task(task_id):
    st.session_state.tasks = [
        t for t in st.session_state.tasks if t["id"] != task_id
    ]


def toggle_task(task_id, done):
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["done"] = done
            break


# -------------------------------
# STATS
# -------------------------------

tasks = st.session_state.tasks
total = len(tasks)
completed = sum(1 for t in tasks if t["done"])
pending = total - completed

col1, col2, col3 = st.columns(3)
col1.metric("Total", total)
col2.metric("Done", completed)
col3.metric("Pending", pending)

st.divider()

# -------------------------------
# ADD TASK FORM
# -------------------------------

st.subheader("➕ Add a New Task")

with st.form("task_form", clear_on_submit=True):
    st.text_input("Task Title", key="title_input")
    st.text_input("Owner Name", key="owner_input")
    st.date_input("Deadline", value=date.today(), key="deadline_input")
    st.checkbox("Is the task completed?", key="status_input")

    submitted = st.form_submit_button("Add Task", type="primary", use_container_width=True)

    if submitted:
        if st.session_state.title_input.strip() and st.session_state.owner_input.strip():
            add_task()
        else:
            st.error("Please enter both the task title and owner.")

st.divider()

# -------------------------------
# TASK LIST
# -------------------------------

st.subheader("📋 Your Tasks")

if not tasks:
    st.info("No tasks yet. Add your first task above!")
else:
    for task in tasks:
        task_id = task["id"]
        with st.container(border=True):
            col_check, col_text, col_delete = st.columns([0.12, 0.73, 0.15])

            is_done = col_check.checkbox(
                "",
                value=task["done"],
                key=f"done_{task_id}",
                label_visibility="collapsed",
            )
            if is_done != task["done"]:
                toggle_task(task_id, is_done)
                st.rerun()

            if task["done"]:
                col_text.markdown(f"~~**{task['title']}**~~ ✅")
            else:
                col_text.markdown(f"**{task['title']}**")
            col_text.caption(f"Owner: {task['owner']}  |  Deadline: {task['deadline']}")

            if col_delete.button("🗑️", key=f"delete_{task_id}", help="Delete task"):
                delete_task(task_id)
                st.rerun()

st.divider()

# -------------------------------
# PICK A RANDOM TASK
# -------------------------------

st.subheader("🎯 Pick a Random Task")

if st.button("Pick Random Task", use_container_width=True):
    incomplete_tasks = [t for t in tasks if not t["done"]]
    if incomplete_tasks:
        picked = random.choice(incomplete_tasks)
        st.info(
            f"🎯 **Random Task:** {picked['title']} — Owner: {picked['owner']}"
            f" | Deadline: {picked['deadline']}"
        )
    elif tasks:
        st.success("🎉 All tasks are completed!")
    else:
        st.warning("No tasks available to pick.")

st.divider()

# -------------------------------
# CLEAR ALL
# -------------------------------

if st.button("🧹 Clear All Tasks", use_container_width=True):
    st.session_state.tasks = []
    st.success("All tasks have been cleared.")
    st.rerun()

st.divider()
st.caption("My To-Do App · Built with Streamlit")
