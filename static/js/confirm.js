new Vue({
    el: '#app',
    computed:{
        now(){
            return Date.now();
        }
    },
    mounted(){
        self = this
        axios.get('/api/formInfo')
            .then(function(response) {
                if(response.data.errno !== 0){
                    self.$message({
                        message: response.data.msg,
                        type: 'error'
                    })
                    return
                }
                data = response.data.data
                self.form.name = data['name'];
                self.form.idCard = data['idCard'];
                self.form.sNumber = data['sNumber'];
                self.form.sex = data['sex'];
                self.form.profession = data['profession'];
                self.form.nation = data['nation'];
                self.form.workUnit = data['workUnit'];
                self.form.department = data['department'];
                self.form.classId = data['classId'];
                self.form.rank = data['rank'];
                self.hasImg = data['hasImg'];
                self.isConfirm= data['isConfirm'];
                self.loading = false;
            })
            .catch(function(error) {
                console.log(error);
            });
    },
    data() {
      return {
      loading: true,
      form: {},
      imageUrl: '',
      hasImg: false,
      isConfirm: false,
      }
    },
    methods: {
      handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
        this.hasImg = true;
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      reLogin(){
        this.$confirm('确定要重新登录吗', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
            axios.get('/api/reLogin').then(function(response){
                window.location = '/';
            });
        })
      },
      confirmError(){
          this.$message({
                          type: 'warning',
                          message: '请联系辅导员或相关老师'
                      });
      },
      confirmInfo(){
          if(!this.hasImg){
              this.$notify.error({
                  title: '错误',
                  message: '请上传个人照片',
              });
              return;
          }
          self = this
          this.$confirm('此操作将确认个人信息, 是否继续?', '提示', {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              axios.post('/api/confirm').then(function(response){
                  data = response.data;
                  if(data.errno === 0){
                      self.$message({
                          type: 'success',
                          message: '信息确认成功!'
                      });
                      self.isConfirm = true;
                  }else{
                      self.$message({
                          type: 'warning',
                          message: '信息已经确认过了, 不要重复确认!'
                      });
                  }
              });
            })
      }
    }
})
