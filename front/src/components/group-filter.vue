<template>
  <div class="filter">
    <Form :model="formItem" :label-width="80">
      <Row>
        <Col span="9">
          <FormItem label="Input">
              <Input v-model="formItem.input" placeholder="Enter something..."></Input>
          </FormItem>
        </Col>
        <Col span="12">
          <FormItem label="DatePicker">
              <Row>
                <Col span="11">
                      <DatePicker type="date" placeholder="Select date" v-model="formItem.date"></DatePicker>
                </Col>
                <Col span="2">
                  <Icon type="ios-arrow-round-forward" size="24"/>
                </Col>
                <Col span="11">
                      <DatePicker type="date" placeholder="Select date" v-model="formItem.date"></DatePicker>
                </Col>
              </Row>
          </FormItem>
        </Col>
      </Row>
        <FormItem label="Radio">
            <RadioGroup v-model="formItem.radio">
                <Radio label="male">Male</Radio>
                <Radio label="female">Female</Radio>
            </RadioGroup>
        </FormItem>
        <FormItem label="Checkbox">
            <CheckboxGroup v-model="formItem.checkbox">
                <Checkbox label="Eat"></Checkbox>
                <Checkbox label="Sleep"></Checkbox>
                <Checkbox label="Run"></Checkbox>
                <Checkbox label="Movie"></Checkbox>
            </CheckboxGroup>
        </FormItem>
        <FormItem label="Switch">
            <i-switch v-model="formItem.switch" size="large">
                <span slot="open">On</span>
                <span slot="close">Off</span>
            </i-switch>
        </FormItem>
        <FormItem label="Slider">
            <Slider v-model="formItem.slider" range></Slider>
        </FormItem>
        <FormItem label="Text">
            <Input v-model="formItem.textarea" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="Enter something..."></Input>
        </FormItem>
        <FormItem>
            <Button type="primary">Submit</Button>
            <Button style="margin-left: 8px">Cancel</Button>
        </FormItem>
    </Form>
  </div>

</template>
<script>
    export default {
        data () {
            return {
                formItem: {
                    input: '',
                    select: '',
                    radio: 'male',
                    checkbox: [],
                    switch: true,
                    date: '',
                    time: '',
                    slider: [20, 50],
                    textarea: ''
                }
            }
        }
    }
</script>
<style scoped>
.filter{
  margin: 25px;
}
</style>
