<template>
    <v-dialog v-model="dialogVisible" width="800px" scrollable>
        <v-card rounded="lg">
            <!-- <a-form layout="vertical" :model="form"> -->
                <v-card-title class="d-flex justify-space-between align-center">
                    <div class="text-h5 text-medium-emphasis ps-2">Add Attachments</div>
                    <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
                </v-card-title>
                <!-- <v-divider class="m-0"></v-divider> -->
                <v-card-text>
                    <Toast />
                    <FileUpload 
                    name="file" 
                    :auto="true" 
                    url="/api/method/upload_file"
                    @before-send="beforeSend"
                    @upload="upload"
                    :multiple="true" 
                    accept="image/*,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    :maxFileSize="1000000"
                    >
                    
                        <template #header="{ chooseCallback, uploadCallback, clearCallback, files }">
                            <div class="d-flex flex-wrap justify-between align-items-center flex-fill gap-3">
                                <div class="d-flex gap-2">
                                    <!-- <Button @click="chooseCallback()" outlined severity="secondary">Attach</Button> -->
                                    <v-btn @click="chooseCallback()" prepend-icon="mdi mdi-upload" color="light-blue">Attach</v-btn>
                                    <!-- <Button @click="uploadEvent(uploadCallback)" icon="pi pi-cloud-upload" rounded outlined severity="success" :disabled="!files || files.length === 0"></Button>
                                    <Button @click="clearCallback()" icon="pi pi-times" rounded outlined severity="danger" :disabled="!files || files.length === 0"></Button> -->
                                </div>
                                <ProgressBar :value="totalSizePercent" :showValue="false" class="md:w-20rem h-1 w-full md:ml-auto">
                                    <span class="whitespace-nowrap">{{ totalSize }}B / 1Mb</span>
                                </ProgressBar>
                            </div>
                        </template>
                        <!-- <template #content="{ files, uploadedFiles, removeUploadedFileCallback, removeFileCallback }">
                            <div class="d-flex flex-column gap-8 pt-4">
                                <div v-if="files.length > 0">
                                    <h5>Pending</h5>
                                    <div class="d-flex flex-wrap gap-4">
                                        <div v-for="(file, index) of files" :key="file.name + file.type + file.size" class="p-8 rounded d-flex flex-column border border-surface align-items-center gap-4">
                                            <div>
                                                <img role="presentation" :alt="file.name" :src="file.objectURL" width="100" height="50" />
                                            </div>
                                            <span class="font-semibold text-ellipsis max-w-60 whitespace-nowrap overflow-hidden">{{ file.name }}</span>
                                            <div>{{ formatSize(file.size) }}</div>
                                            <Badge value="Pending" severity="warn" />
                                            <Button icon="pi pi-times" @click="onRemoveTemplatingFile(file, removeFileCallback, index)" outlined rounded severity="danger" />
                                        </div>
                                        <DataTable :value="products" tableStyle="min-width: 50rem">
                                            <template #header>
                                                <div class="flex flex-wrap items-center justify-between gap-2">
                                                    <span class="text-xl font-bold">Products</span>
                                                    <Button icon="pi pi-refresh" rounded raised />
                                                </div>
                                            </template>
                                            <Column field="name" header="Name"></Column>
                                            <Column header="Image">
                                                <template #body="slotProps">
                                                    <img :src="`https://primefaces.org/cdn/primevue/images/product/${slotProps.data.image}`" :alt="slotProps.data.image" class="w-24 rounded" />
                                                </template>
                                            </Column>
                                            <Column field="price" header="Price">
                                                <template #body="slotProps">
                                                    {{ formatCurrency(slotProps.data.price) }}
                                                </template>
                                            </Column>
                                            <Column field="category" header="Category"></Column>
                                            <Column field="rating" header="Reviews">
                                                <template #body="slotProps">
                                                    <Rating :modelValue="slotProps.data.rating" readonly />
                                                </template>
                                            </Column>
                                            <Column header="Status">
                                                <template #body="slotProps">
                                                    <Tag :value="slotProps.data.inventoryStatus" :severity="getSeverity(slotProps.data)" />
                                                </template>
                                            </Column>
                                            <template #footer> In total there are {{ products ? products.length : 0 }} products. </template>
                                        </DataTable>
                                    </div>
                                </div>

                                <div v-if="uploadedFiles.length > 0">
                                    <h5>Completed</h5>
                                    <div class="d-flex flex-wrap gap-4">
                                        <div v-for="(file, index) of uploadedFiles" :key="file.name + file.type + file.size" class="p-8 rounded d-flex flex-column border border-surface align-items-center gap-4">
                                            <div>
                                                <img role="presentation" :alt="file.name" :src="file.objectURL" width="100" height="50" />
                                            </div>
                                            <span class="font-semibold text-ellipsis max-w-60 whitespace-nowrap overflow-hidden">{{ file.name }}</span>
                                            <div>{{ formatSize(file.size) }}</div>
                                            <Badge value="Completed" class="mt-4" severity="success" />
                                            <Button icon="pi pi-times" @click="removeUploadedFileCallback(index)" outlined rounded severity="danger" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template> -->
                        <template #empty>
                            <div class="d-flex align-items-center justify-center flex-column">
                                <i 
                                class="pi pi-cloud-upload border-2 rounded-circle p-8 text-4xl text-muted-color" 
                                style="color: #64748b; font-size: 2.25rem; line-height: 2.5rem; padding: 2rem; border-style: solid;"
                                />
                                <p class="mt-6 mb-0">Drag and drop files here to upload.</p>
                            </div>
                        </template>
                    </FileUpload>
                </v-card-text>
                <v-divider class="mt-2"></v-divider>
                <v-card-actions class="my-2 d-flex justify-end">
                <v-btn
                class="text-none"
                text="Cancel"
                @click="closeDialog"
                ></v-btn>
                <v-btn
                class="text-none"
                color="blue"
                
                text="Add"
                variant="tonal"
                @click="onSubmit()"
                type="submit"
                ></v-btn>
                </v-card-actions>
            <!-- </a-form> -->
        </v-card>
    </v-dialog>
</template>

<script >
import dayjs from 'dayjs';
import { reactive, ref } from 'vue';

import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';


export default {
	inject: ['$call'],
	components: {
		VDivider, VContainer, VCol, VRow, VInfiniteScroll, VItemGroup, VItem,
	},
	props: {
		isOpen: {
            type: Boolean,
            required: true,
            default: false,
        },
        doctype: {
            type: String,
            default: '',
        },
        docname: {
            type: String,
            default: '',
        },
        fieldName: {
            type: String,
            default: '',
        },
        parent: {
            type: String,
            default: '',
        },
        parentType: {
            type: String,
            default: '',
        },
        isChild: {
            type: Boolean,
            default: false,
        }
	},
    computed: {
        dialogVisible: {
            get() {
                return this.isOpen;
            },
            set(value) {
                this.$emit('update:isOpen', value);
            },
        },
    },
	data() {
		return {
            files: [],
            totalSize: 0,
            totalSizePercent: 0,
            fileDocname: '',
            file_url: '',
            fileName: '',
		};
	},
	methods: {
        updateIsOpen(value) {
            this.$emit('update:isOpen', value);
        },
        closeDialog() {
            this.updateIsOpen(false);
        },
        onCellEditComplete(event) {
            let { data, newValue, field } = event;

            switch (field) {
                case 'quantity':
                case 'price':
                    if (this.isPositiveInteger(newValue)) data[field] = newValue;
                    else event.preventDefault();
                    break;

                default:
                    if (newValue.trim().length > 0) data[field] = newValue;
                    else event.preventDefault();
                    break;
            }
        },
        beforeSend(event) {
            if(this.isChild){
                event.formData.append('doctype', this.parentType);
                event.formData.append('docname', this.parent);
                event.formData.append('fieldname', this.fieldName);
                event.formData.append('is_private', '1');
            }
            else{
                event.formData.append('doctype', this.doctype);
                event.formData.append('docname', this.docname);
                event.formData.append('fieldname', this.fieldName);
                event.formData.append('is_private', '1');
            }
        },
        upload(event) {
            const doc = JSON.parse(event.xhr.response).message;
            this.fileDocname = doc.name
            this.file_url = doc.file_url
            this.fileName = doc.file_name.split('.')[0]
        },
        onSubmit() {
            if(this.isChild){
                const doc = {
                    doctype: this.doctype, 
                    parent: this.parent, 
                    parentfield: this.fieldName, 
                    parenttype: this.parentType, 
                    attachment: this.file_url,
                    attachment_name: this.fileName
                }
                console.log(doc)
                this.$call('frappe.client.insert', {doc})
                .then(response => {
                    this.closeDialog()
                }).catch(error => {
                    console.error(error);
                    let message = error.message.split('\n');
                    message = message.find(line => line.includes('frappe.exceptions'));
                    if(message){
                        const firstSpaceIndex = message.indexOf(' ');
                        this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
                    }
                });
            }
            else{
                const form = {
                    doctype: this.doctype, 
                    docname: this.docname, 
                    [this.fieldName]: 'hi', 
                }
                this.$call('healthcare_doworks.api.methods.edit_doc', {form})
                .then(response => {
                    this.closeDialog()
                }).catch(error => {
                    console.error(error);
                    let message = error.message.split('\n');
                    message = message.find(line => line.includes('frappe.exceptions'));
                    if(message){
                        const firstSpaceIndex = message.indexOf(' ');
                        this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
                    }
                });
            }
        }
	},
};
</script>