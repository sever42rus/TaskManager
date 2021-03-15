<template>
  <div>
    <div class="modal modalb" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Добавление задачи</h5>
          </div>
          <div class="modal-body">
            <input
              type="text"
              class="form-control"
              v-model="form.title"
              placeholder="Заголовок"
            />
            <input
              type="text"
              class="form-control"
              v-model="form.text"
              placeholder="Текст"
            />
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="$emit('close')"
            >
              Close
            </button>
            <button type="button" class="btn btn-primary" @click="save()">
              Save changes
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
 
<script>
export default {
  name: "ModalWindow",
  data: function () {
    return {
      form: {},
      formError: {},
    };
  },
  props: {
    source: String,
    method: String,
  },
  async mounted() {
    fetch(this.source)
      .then((response) => {
        if (!response.ok) {
          this.$emit("close");
          return 0;
        }
        return response.json();
      })
      .then((data) => {
        this.form = data;
      });
  },
  methods: {
    async save() {
      console.log(this.form);
      const response = await fetch(this.source, {
        method: this.method,
        body: JSON.stringify(this.form),
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      });
      if (response.ok) {
        this.$emit("save");
      } else {
        this.formError = await response.json();
        console.log(this.formError);
      }
    },
  },
};
</script>
 
<style>
.modalb {
  display: block;
}
</style>