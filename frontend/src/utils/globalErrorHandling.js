export default {
  data() {
    return {
      alertMessage: '',
      alertType: '', // 'success' or 'error'
      showAlert: false
    };
  },
  methods: {
    showAlertMessage(type, message) {
      this.alertType = type;
      this.alertMessage = message;
      this.showAlert = true;

      // Automatically hide the alert after a few seconds (optional)
      setTimeout(() => {
        this.showAlert = false;
      }, 3000);
    },
    handleSuccess(message) {
      this.showAlertMessage('success', message || 'Operation completed successfully');
    },
    handleError(error) {
      let errorMessage = 'An unexpected error occurred';
      if (error.response && error.response.data && error.response.data._server_messages) {
        const serverMessages = JSON.parse(error.response.data._server_messages);
        errorMessage = serverMessages.join(', ');
      }
      this.showAlertMessage('error', errorMessage);
    }
  }
};