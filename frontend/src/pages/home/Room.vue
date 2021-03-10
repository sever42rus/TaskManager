<template>
  <div class="container">
    <div class="row justify-content-center mt-4">
      <div class="col-6">
        <div class="form-group">
          <div class="input-group">
            <input
              type="input"
              class="form-control m-1"
              placeholder="Назавание новой колонки"
              v-model="columnCreateName"
            />
            <button
              class="btn btn-success m-1"
              v-on:click="backendColumnCreate()"
            >
              Создать
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div v-for="column in columns" :key="column.id" class="col-4 mt-4 mb-4">
        <div
          class="card"
          @drop="onDrop($event, column)"
          @dragenter.prevent
          @dragover.prevent
        >
          <h4 class="card-header">{{ column.name }}</h4>
          <button
            class="btn btn-danger"
            v-on:click="backendColumnRemove(column.id)"
          >
            Удалить
          </button>
          <button
            class="btn btn-primary"
            v-on:click="
              showModal = true;
              modalMethod = 'POST';
              modalSource = `/task/task/form/${column.id}/`;
            "
          >
            Добавить задание
          </button>
          <div class="card-body">
            <div
              draggable="true"
              class="m-3"
              v-for="task in column.task"
              :key="task.id"
              @dragstart="startDrag($event, task)"
            >
              <div class="card">
                <h5 class="card-header">{{ task.title }}</h5>
                <button
                  class="btn btn-danger"
                  v-on:click="backendTaskRemove(task.id)"
                >
                  Удалить
                </button>
                <button
                  class="btn btn-primary"
                  v-on:click="
                    showModal = true;
                    modalMethod = 'PUT';
                    modalSource = `/task/task/edit/${task.id}/`;
                  "
                >
                  Изменить
                </button>
                <div class="card-body">
                  <p>{{ task.title }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Form
      v-if="showModal"
      @close="hideModalForm"
      @save="saveModalForm"
      :source="modalSource"
      :method="modalMethod"
    ></Form>
  </div>
</template>


<script>
import Form from "./Form.vue";

export default {
  name: "Home",
  components: {
    Form,
  },
  data: () => ({
    columns: Object,
    moveTask: Object,
    columnCreateName: "",
    showModal: false,
    modalSource: "",
    modalMethod: "",
    roomId: localStorage.getItem("room"),
  }),
  async mounted() {
    await this.reload();
  },
  methods: {
    async reload() {
      const response = await fetch(`/task/column/list/${this.roomId}/`);
      if (response.ok) {
        this.columns = await response.json();
      } else {
        console.log("errors!");
      }
    },

    async movingTaskBackend(taskId, columnId) {
      const response = await fetch(`/task/task/moving/${taskId}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          room_column: columnId,
        }),
      });
      if (response.ok) {
        return true;
      } else {
        return false;
      }
    },

    startDrag(evt, task) {
      this.moveTask = task;
    },

    async onDrop(evt, target) {
      var backendStatus = await this.movingTaskBackend(
        this.moveTask.id,
        target.id
      );
      if (backendStatus) this.reload();
      /* if (backendStatus) {
        for (var i in this.columns) {
          for (var j in this.columns[i].task) {
            if (this.columns[i].task[j].id == this.moveTask.id) {
              this.columns[i].task.splice(j, 1);
            }
          }
          if (this.columns[i].id == target.id) {
            this.columns[i].task.push(this.moveTask);
          }
        }
      } */
    },

    async backendColumnCreate() {
      const response = await fetch(`/task/column/form/${this.roomId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: this.columnCreateName,
          room: this.roomId,
        }),
      });
      if (response.ok) {
        this.columnCreateName = "";
        this.reload();
      }
    },
    async backendColumnRemove(target) {
      const response = await fetch(
        `/task/column/edit/${this.roomId}/${target}/`,
        {
          method: "DELETE",
        }
      );
      if (response.ok) {
        this.reload();
      }
    },
    async backendTaskRemove(target) {
      const response = await fetch(`/task/task/edit/${target}/`, {
        method: "DELETE",
      });
      if (response.ok) {
        this.reload();
      }
    },
    showModalForm() {
      this.showModal = true;
      this.modalSource = "/tu/home/";
    },
    hideModalForm() {
      this.showModal = false;
    },
    saveModalForm() {
      this.showModal = false;
      this.reload();
    },
  },
};
</script>

<style>
</style>