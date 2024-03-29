new Vue({
    el: '#app',
    data: {
      sNumber: '',
      password: ''
    },
    methods: {
      check: function() {
        //获取值
        var sNumber = this.sNumber;
        var password = this.password;
        let self = this
        if (sNumber == '' || password == '') {
          this.$message({
            message: '账号或密码为空！',
            type: 'warning'
          })
          return;
        }
        axios.post('/api/loginCheck', {
            sNumber,
            password
          })
          .then(function(response) {
              let data = response.data
              if(data['errno']==0){
                  self.$message({
                      message: '登陆成功',
                      type: 'success'
                  })
                  location.href = '/confirm';
              }else{
                  self.$message({
                      message: '用户名或密码错误',
                      type: 'error'
                  })
              }
          })
          .catch(function(error) {
            console.log(error);
          });

      },
      forget:function(){
          this.$message({
              message: '默认密码是身份证后六位!',
              type: 'warning'
          })
      }
    }
  })