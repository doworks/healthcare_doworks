import React, { useState, useEffect } from 'react';
import { Excalidraw, Sidebar, Footer, exportToBlob, exportToClipboard } from '@excalidraw/excalidraw';
import call from "../../utils/reactCall";

import { 
  List, ListItemDecorator, ListItemButton, Tabs, TabList, Tab, TabPanel, Radio, 
  RadioGroup, Sheet, Button, Badge, Option, FormLabel, Input, Card,
} from '@mui/joy';
import AspectRatio from '@mui/joy/AspectRatio';
import Box from '@mui/joy/Box';
import Drawer from '@mui/joy/Drawer';
import CardContent from '@mui/joy/CardContent';
import Checkbox from '@mui/joy/Checkbox';
import DialogTitle from '@mui/joy/DialogTitle';
import DialogContent from '@mui/joy/DialogContent';
import ModalClose from '@mui/joy/ModalClose';
import Divider from '@mui/joy/Divider';
import FormControl from '@mui/joy/FormControl';
import FormHelperText from '@mui/joy/FormHelperText';
import ListItem from '@mui/joy/ListItem';
import Stack from '@mui/joy/Stack';
import Switch from '@mui/joy/Switch';
import Typography from '@mui/joy/Typography';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import ApartmentRoundedIcon from '@mui/icons-material/ApartmentRounded';
import MeetingRoomRoundedIcon from '@mui/icons-material/MeetingRoomRounded';
import HotelRoundedIcon from '@mui/icons-material/HotelRounded';
import Done from '@mui/icons-material/Done';

import { tabClasses } from '@mui/joy/Tab';
import { radioClasses } from '@mui/joy/Radio';
import CheckCircleRoundedIcon from '@mui/icons-material/CheckCircleRounded';
import Select from 'react-select'

const generateFileId = (img) => {
  // Generate a unique fileId using a combination of the image name and a timestamp or any other unique identifier
  return `${img.name}-${Date.now()}`;
};

const ExcalidrawWrapper = () => {
  const [index, setIndex] = useState(0);
  const [excalidrawAPI, setExcalidrawAPI] = useState(null);
  const [drawingsSidebar, setDrawingsSidebar] = useState(true);
  const [treatmentSidebar, setTreatmentSidebar] = useState(false);
  const [historyOpen, setHistoryOpen] = React.useState(false);
  const [selectedTreatment, setSelectedTreatment] = useState('')
  const [newElement, setNewElement] = useState('')
  const [selectedElement, setSelectedElement] = useState('')
  const [variables, setVariables] = useState({})
  const [images, setImages] = useState({male:[], female:[]});
  const [treatments, setTreatments] = useState([]);
  const [annotationHistory, setAnnotationHistory] = useState([]);
  const [annotationsTemplate, setAnnotationsTemplate] = useState('');
  useEffect(() => {
    call('healthcare_doworks.api.methods.annotations_records')
    .then(response => {
      let vars = {}
      response.treatments.forEach(treatment => {
        vars[treatment.treatment] = {}
        treatment.variables.forEach(value => {
          vars[treatment.treatment][value.variable_name] = ''
        })
      })
      setVariables(vars)
      setTreatments(response.treatments)
      setImages({
        male: response.templates.filter(doc => doc.gender === 'Male'),
        female: response.templates.filter(doc => doc.gender === 'Female'),
      })
    }).catch(error => {
      console.error(error);
    });
  }, []);

  useEffect(() => {
    const handleSave = async (event) => {
      if (!excalidrawAPI) {
        return
      }
  
      const elements = excalidrawAPI.getSceneElements();
      if (!elements || !elements.length) {
        return;
      }
  
      // Export as Blob
      const blob = await exportToBlob({
        elements,
        appState: excalidrawAPI.getAppState(),
        files: excalidrawAPI.getFiles(),
        mimeType: 'image/jpeg'
      });
  
      // Create JSON directly instead of relying on clipboard
      const jsonText = JSON.stringify({
        elements,
        files: excalidrawAPI.getFiles(),
      });
  
      const { callback } = event.detail;
      const url = URL.createObjectURL(blob);
  
      callback({ annotationsTemplate, url, jsonText, blob });
  };

    const setAnnotationHistoryState = async (event) => {
      const { annotations } = event.detail;
      setAnnotationHistory(annotations.map(value => {
        value.data = JSON.parse(value.json)
        return value
      }))
    };

    window.addEventListener('reactSaveAnotation', handleSave);
    window.addEventListener('reactSetAnnotationHistory', setAnnotationHistoryState);

    // Clean up the event listener on unmount
    return () => {
      window.removeEventListener('reactSaveAnotation', handleSave);
      window.removeEventListener('reactSetAnnotationHistory', setAnnotationHistoryState);
    };

  }, [excalidrawAPI, annotationsTemplate]);

  const updateElementCustomData = (target, newVars) => {
    const sceneElements = excalidrawAPI.getSceneElements().map(element => {
      if(element.id === target.id){
        if(newVars)
          element.customData = newVars
        else
          element.customData = {...variables[selectedTreatment], type: selectedTreatment}
      }
      return element
    })
  
    excalidrawAPI.updateScene({
      elements: sceneElements
    })
  }

  const handleExcaliChange = (elements, appState) => {
    const newElements = appState.editingElement
    const cursorButton = appState.cursorButton
    if(treatmentSidebar && selectedTreatment && appState.activeTool.type !== 'freedraw' && appState.activeTool.type !== 'selection' && !selectedElement){
      setSelectedTreatment('')
      // console.log('hi')
      // excalidrawAPI.updateScene({
      //   ...appState,
      //   currentItemStrokeColor: '#1e1e1e',
      // })
      excalidrawAPI.toggleSidebar({name: 'drawings'})
    }
    if (newElements && newElements.type === 'freedraw') {
      setNewElement(newElements)
    }
    if (newElement && cursorButton === 'up' && excalidrawAPI) {
      updateElementCustomData(newElement)    
      setNewElement(null)
    }
  };

  const handleExcaliPointerDown = (activeTool, pointerDownState) => {
    const thisElement = pointerDownState.hit.element;
    if (thisElement && thisElement.type === 'freedraw') {
      setVariables({...variables, [thisElement.customData.type]: thisElement.customData})
      setSelectedElement(thisElement)
      setSelectedTreatment(thisElement.customData.type)
    }
    else{
      if(activeTool.type === "selection"){
        setSelectedElement('')
        setSelectedTreatment('')
      }
    }
  };

  const handleDrawModeClick = (treatment) => {
    if (!excalidrawAPI) return;

    setSelectedTreatment(treatment.treatment);
    excalidrawAPI.updateScene({
      appState: {
        ...excalidrawAPI.getAppState(),
        activeTool: {
          type: "freedraw",
        },
        currentItemStrokeColor: treatment.color, // Set your desired stroke color here
      },
      commitToHistory: true,
    });
    // excalidrawAPI.scrollToContent()
    // excalidrawAPI.refresh()
  };

  const importAnnotation = (annotation) => {
    if (!excalidrawAPI) return;
    
    console.log(annotation)
    for (const [key, value] of Object.entries(annotation.data.files)) {
      excalidrawAPI.addFiles([value]);
    }
    excalidrawAPI.updateScene(annotation.data);
    excalidrawAPI.scrollToContent()
    excalidrawAPI.refresh()
    setHistoryOpen(false)
  };

  const handleImageClick = async (img, array, gender) => {
    if (!excalidrawAPI) return;

    const canvasContainer = document.querySelector('.excalidraw__canvas'); // Assuming Excalidraw canvas has this class
    const canvasHeight = canvasContainer.clientHeight;
    const canvasWidth = canvasContainer.clientWidth;
    setAnnotationsTemplate(img.name)
    const image = new Image();
    image.src = img.image;
    image.onload = () => {
      const canvas = document.createElement('canvas');
      canvas.width = image.width; // Set canvas width to image width
      canvas.height = image.height; // Set canvas height to image height
      const ctx = canvas.getContext('2d');
      ctx.drawImage(image, 0, 0);
  
      const dataURL = canvas.toDataURL('image/jpeg'); // Ensure the data URL is in JPEG format  
      let fileId = img.id;
      if (!img.id) { // Check if fileId exists
        fileId = generateFileId(img); // Generate a unique fileId
        excalidrawAPI.addFiles([{
          mimeType: 'image/jpeg',
          id: fileId,
          dataURL: dataURL,
          created: Date.now(),
        }]);
        if(array){
          const newArray = array.map(val => {
            if (val.image === img.image) val.id = fileId;
            return val;
          });

          setImages({ ...images, [gender]: newArray });
        }
      }

      const scaleFactor = canvasHeight / image.height;
      const imageWidth = image.width * scaleFactor;
      const imageHeight = canvasHeight;
      const imageX = (canvasWidth - imageWidth) / 2;
      const imageY = (canvasHeight - imageHeight) / 2;
  
      const imageElement = {
        type: 'image',
        version: 1,
        versionNonce: 123456,
        isDeleted: false,
        id: img.label,
        fillStyle: 'solid',
        strokeWidth: 2,
        strokeStyle: 'solid',
        roughness: 1,
        opacity: 100,
        angle: 0,
        x: imageX,
        y: imageY,
        width: image.width, // Set width to image width
        height: image.height, // Set height to image height
        seed: 1,
        groupIds: [], // Initialize groupIds as an empty array
        dataURL: dataURL, // Ensure the property is correctly named dataURL
        status: 'pending', // Match the status of the successful image
        backgroundColor: 'transparent', // Set a default background color
        strokeColor: 'transparent', // Set a default stroke color
        boundElements: null, // Match the boundElements property
        customData: undefined, // Match the customData property
        fileId: fileId,
        frameId: null, // Match the frameId property
        link: null, // Match the link property
        locked: true, // Match the locked property
        roundness: null, // Match the roundness property
        scale: [scaleFactor, scaleFactor], // Set scale to fit height
        updated: Date.now(), // Use the current timestamp for the updated property
      };
  
      excalidrawAPI.updateScene({
        elements: [imageElement],
        commitToHistory: true,
      });
      excalidrawAPI.scrollToContent()
      excalidrawAPI.refresh()
    };
  
    image.onerror = (error) => {
      console.error('Failed to load image:', error);
    };
  };

  return (
    <div style={{ height: '100%' }}>
      <div className={'excalidraw-wrapper ' + (selectedTreatment ? 'leftdrawer-open' : '')} style={{ height: '100%', position: 'relative'}}>
        {selectedTreatment && <Card variant='soft' sx={{ width: 240, zIndex: 10, marginTop: '40px', height: 'fit-content', position: 'absolute'}}>
          {treatments.find(treatment => treatment.treatment == selectedTreatment).variables.map((variable, index) => {
            if(variable.type === 'Select'){
              let optionsArray = variable.options.split('\n')
              variable.selectOptions = optionsArray.map(option => {return {label: option, value: option}})
            }
            return <div key={index}>
              <FormLabel>{variable.variable_name}</FormLabel>
              {variable.type === 'Select' ? 
                <Select 
                name={variable.variable_name}
                isClearable
                value={variable.selectOptions.find(option => option.value === variables[selectedTreatment][variable.variable_name]) || ''}
                onChange={(selectedOption) => {
                  const newVars = {
                    ...variables[selectedTreatment],
                    [variable.variable_name]: selectedOption ? selectedOption.value : ''
                  }
                  setVariables({...variables, [selectedTreatment]: newVars});
                  if(selectedElement)
                    updateElementCustomData(selectedElement, newVars)
                }}
                options={variable.selectOptions}
                />
              : variable.type === 'Data' ? <Input value={variables[selectedTreatment][variable.variable_name]} onChange={event => {
                const newVars = {
                  ...variables[selectedTreatment],
                  [variable.variable_name]: event.target.value
                }
                setVariables({...variables, [selectedTreatment]: newVars});
                if(selectedElement)
                  updateElementCustomData(selectedElement, newVars)
              }}/> 
              : <></>}
            </div>
          })}
        </Card>}
        <Excalidraw
        onChange={handleExcaliChange}
        onPointerDown={handleExcaliPointerDown}
        excalidrawAPI={(api)=> setExcalidrawAPI(api)}
        initialData={{
          elements: [],
          appState: {
            openSidebar: { name: 'drawings' },
          },
          scrollToContent: true
        }}
        renderTopRightUI={() => { 
          return (
            <>
              {!drawingsSidebar && <Button name="drawings" variant="soft" onClick={() => {excalidrawAPI.toggleSidebar({name: 'drawings'})}}>
                Drawings
              </Button>}
              {!treatmentSidebar && <Button 
              name="treatments" 
              color="success" 
              variant="soft" 
              onClick={() => {excalidrawAPI.toggleSidebar({name: 'treatments'})}}
              >
                Treatments
              </Button>}
            </>
          );
        }}
        >
          <Sidebar name="drawings" className='drawings-sidebar' docked onStateChange={setDrawingsSidebar}>
            <Sidebar.Tabs>
              <Tabs
                value={index}
                onChange={(event, value) => setIndex(value)}
                sx={(theme) => ({
                  m: 1,
                  borderRadius: 16,
                  height: '100%',
                  boxShadow: theme.shadow.md,
                  
                  [`& .${tabClasses.root}`]: {
                    py: 1,
                    flex: 1,
                    transition: '0.3s',
                    fontWeight: 'md',
                    fontSize: 'md',
                    [`&:not(.${tabClasses.selected}):not(:hover)`]: {
                      opacity: 0.7,
                    },
                  },
                })}
              >
                <TabList
                  variant="plain"
                  size="sm"
                  disableUnderline
                  sx={{ borderRadius: 'xl', p: 2 }}
                >
                  <Tab
                    disableIndicator
                    {...(index === 0 && { color: 'primary' })}
                  >
                    Male
                  </Tab>
                  <Tab
                    disableIndicator
                    {...(index === 1 && { color: 'danger' })}
                  >
                    Female
                  </Tab>
                </TabList>
                <TabPanel value={0} sx={{ p: 0 }}>
                  <div>
                    <List style={{height: 'calc(100vh - 175px)',overflowY: 'auto'}}>
                      {images.male.map((img, index, array) => (
                        <ListItemButton key={img.label} onClick={() => {handleImageClick(img, array, 'male')}}>
                          <ListItemDecorator>
                            <img src={img.image} alt={img.label} style={{ width: '50px', height: '50px', marginRight: '15px' }} />
                          </ListItemDecorator>
                          {img.label}
                        </ListItemButton>
                      ))}
                    </List>
                  </div>
                </TabPanel>
                <TabPanel value={1} sx={{ p: 0 }}>
                  <div>
                    <List>
                      {images.female.map((img, index, array) => (
                        <ListItemButton key={img.label} onClick={() => {handleImageClick(img, array, 'female')}}>
                          <ListItemDecorator>
                            <img src={img.image} alt={img.label} style={{ width: '50px', height: '50px', marginRight: '15px' }} />
                          </ListItemDecorator>
                          {img.label}
                        </ListItemButton>
                      ))}
                    </List>
                  </div>
                </TabPanel>
              </Tabs>
            </Sidebar.Tabs>
          </Sidebar>

          <Sidebar name="treatments" className='treatments-sidebar' docked onStateChange={setTreatmentSidebar}>
            <RadioGroup
            overlay
            name="treatments"
            sx={{
              display: 'flex',
              flexWrap: 'wrap',
              flexDirection: 'row',
              padding: '1rem',
              gap: 2,
              [`& .${radioClasses.checked}`]: {
                [`& .${radioClasses.action}`]: {
                  inset: -1,
                  border: '3px solid',
                  borderColor: 'primary.500',
                },
              },
              [`& .${radioClasses.radio}`]: {
                display: 'contents',
                '& > svg': {
                  zIndex: 2,
                  position: 'absolute',
                  top: '-8px',
                  right: '-8px',
                  bgcolor: 'background.surface',
                  borderRadius: '50%',
                },
              },
            }}
            >
              {treatments.map((value, index) => (
                <Sheet
                  key={index}
                  variant="outlined"
                  sx={{
                    borderRadius: 'md',
                    boxShadow: 'sm',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: 1.5,
                    p: 2,
                    minWidth: 120,
                  }}
                  onClick={() => {handleDrawModeClick(value)}}
                >
                  <Badge sx={{
                    marginRight: 'auto',
                    ['& .MuiBadge-badge']: {
                      backgroundColor: value.color
                    }
                  }}>
                  </Badge>
                  <Radio id={value.treatment} value={value.treatment} checkedIcon={<CheckCircleRoundedIcon />}/>
                  {value.treatment}
                </Sheet>
              ))}
            </RadioGroup>
          </Sidebar>

          <Footer>
            <Button color="neutral" onClick={() => setHistoryOpen(true)}>
              History
            </Button>
            <Drawer
              size="md"
              variant="plain"
              open={historyOpen}
              onClose={() => setHistoryOpen(false)}
              slotProps={{
                root: { sx: { zIndex: 3000 } },
                content: {
                  sx: {
                    bgcolor: 'transparent',
                    p: { md: 3, sm: 0 },
                    boxShadow: 'none'
                  },
                },
              }}
            >
              <Sheet
                sx={{
                  borderRadius: 'md',
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 2,
                  height: '100%',
                  overflow: 'auto',
                }}
              >
                <DialogTitle>History</DialogTitle>
                <ModalClose />
                <Divider sx={{ mt: 'auto' }} />
                <DialogContent sx={{ gap: 2 }}>
                  <List style={{height: 'calc(100vh - 175px)',overflowY: 'auto'}}>
                    {annotationHistory.map((value, index, array) => (
                      <ListItemButton key={index} onClick={() => {importAnnotation(value)}}>
                        <ListItemDecorator>
                          <img src={value.image} alt={value.name} style={{ width: '50px', height: '50px', marginRight: '15px' }} />
                        </ListItemDecorator>
                        {value.creation}
                      </ListItemButton>
                    ))}
                  </List>
                </DialogContent>

                {/* <Divider sx={{ mt: 'auto' }} />
                <Stack
                  direction="row"
                  useFlexGap
                  spacing={1}
                  sx={{ justifyContent: 'space-between' }}
                >
                  <Button onClick={() => setHistoryOpen(false)}>Show 165 properties</Button>
                </Stack> */}
              </Sheet>
            </Drawer>
          </Footer>
        </Excalidraw>
      </div>
    </div>
  );
};

export default ExcalidrawWrapper;