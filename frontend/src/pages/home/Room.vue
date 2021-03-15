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
        <div class="card">
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
            <div v-if="!column.task.length">
              <div
                @drop="dropColumn($event, column)"
                @dragenter.prevent
                @dragover.prevent
                style="height: 100px"
              ></div>
            </div>
            <div
              draggable="true"
              class="m-3"
              v-for="task in column.task"
              :key="task.id"
              @dragstart="startDrag($event, task)"
              @drop="dropTask($event, task)"
              @dragenter.prevent
              @dragover.prevent
            >
              <div class="card">
                <h5 class="card-header">{{ task.title }}</h5>
                <p class="card-header">Создано: {{ task.created_date }}</p>
                <p class="card-header">
                  Пользователь: {{ task.user_edit.ini }}
                </p>

                <div class="card-body">
                  <p>{{ task.title }}</p>
                </div>
                <div class="card-header d-flex justify-content-center">
                  <button
                    class="btn btn-primary m-2"
                    v-on:click="
                      showModal = true;
                      modalMethod = 'PUT';
                      modalSource = `/task/task/edit/${task.id}/`;
                    "
                  >
                    Изменить
                  </button>
                  <button
                    class="btn btn-danger m-2"
                    v-on:click="backendTaskRemove(task.id)"
                  >
                    Удалить
                  </button>
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

    async movingTaskBackend(whatTaskID, whereTaskID, columnId) {
      const response = await fetch(`/task/task/moving/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          whatTask: whatTaskID,
          whereTask: whereTaskID,
          whereColumn: columnId,
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

    async dropColumn(evt, target) {
      var backendStatus = await this.movingTaskBackend(
        this.moveTask.id,
        null,
        target.id
      );
      if (backendStatus) this.reload();
    },
    async dropTask(evt, target) {
      var backendStatus = await this.movingTaskBackend(
        this.moveTask.id,
        target.id,
        null
      );
      if (backendStatus) this.reload();
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