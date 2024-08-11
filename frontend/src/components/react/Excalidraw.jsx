import React, { useState, useEffect, useCallback } from 'react';
import { Excalidraw, Sidebar, exportToBlob } from '@excalidraw/excalidraw';

import MaleFace3D from '@/assets/img/chartings/3d-male-face.jpeg';
import MaleBodyFB3d from '@/assets/img/chartings/body F&B.jpg';
import BodyFemale from '@/assets/img/chartings/Body female.jpeg';
import BodyMale from '@/assets/img/chartings/Body male.jpeg';
import BodyMaleAndFemale from '@/assets/img/chartings/Body male and female.jpeg';
import FaceAndScalpFemale from '@/assets/img/chartings/Face and scalp female.jpeg';
import FaceFemale1 from '@/assets/img/chartings/Face female 1.jpeg';
import FaceFemale2 from '@/assets/img/chartings/Face female 2.jpeg';
import Head from '@/assets/img/chartings/Head.jpeg';

import { 
  List, ListItemDecorator, ListItemButton, Tabs, TabList, Tab, TabPanel, Radio, 
  RadioGroup, Sheet, Button, Badge, Option, FormLabel, Input, Card,
} from '@mui/joy';
// import { CssVarsProvider, extendTheme } from '@mui/joy/styles';
import { tabClasses } from '@mui/joy/Tab';
import { radioClasses } from '@mui/joy/Radio';
import CheckCircleRoundedIcon from '@mui/icons-material/CheckCircleRounded';
import Select from 'react-select'


const generateFileId = (img) => {
  // Generate a unique fileId using a combination of the image name and a timestamp or any other unique identifier
  return `${img.name}-${Date.now()}`;
};
const Applications = [
  {
    name: 'Laser',
    color: '#1971c2'
  },
  {
    name: 'Mesotherapy',
    color: '#ffd43b'
  },
  {
    name: 'Botox',
    color: '#e03131'
  },
  {
    name: 'Fillers',
    color: '#69db7c'
  },
  {
    name: 'Neofound',
    color: '#f783ac'
  },
  {
    name: 'Other',
    color: '#868e96'
  },
]

const LaserVariables = [
  {
    label: "Fluence", 
    name: "fluence", 
    type: "select", 
    options: [
      { value: '1', label: '1' },
      { value: '2', label: '2' },
      { value: '3', label: '3' },
      { value: '4', label: '4' },
      { value: '5', label: '5' },
      { value: '6', label: '6' },
      { value: '7', label: '7' },
      { value: '8', label: '8' },
      { value: '9', label: '9' },
    ]
  },
  {
    label: "Spot Size", 
    name: "spot_size", 
    type: "select", 
    options: [
      { value: '2', label: '2' },
      { value: '3', label: '3' },
      { value: '4', label: '4' },
      { value: '5', label: '5' },
      { value: '6', label: '6' },
      { value: '7', label: '7' },
      { value: '8', label: '8' },
      { value: '9', label: '9' },
      { value: '10', label: '10' },
    ]
  },
  {
    label: "Pulse Duration", 
    name: "pulse_duration", 
    type: "select", 
    options: [
      { value: '15s', label: '15s' },
      { value: '20s', label: '20s' },
      { value: '25s', label: '25s' },
      { value: '30s', label: '30s' },
      { value: '35s', label: '35s' },
      { value: '40s', label: '40s' },
      { value: '45s', label: '45s' },
    ]
  },
  {
    label: "Repetition Rate", 
    name: "repetition_rate", 
    type: "select", 
    options: [
      { value: '1', label: '1' },
      { value: '2', label: '2' },
      { value: '3', label: '3' },
      { value: '4', label: '4' },
    ]
  },
  {
    label: "No Of Pulses", 
    name: "no_of_pulses", 
    type: "select", 
    options: [
      { value: '1', label: '1' },
      { value: '2', label: '2' },
      { value: '3', label: '3' },
    ]
  }
]

const InjectableVars = [
  {
    label: 'Injectable',
    name: 'injectable',
    type: 'select',
    options: [
      { value: 'Botox', label: 'Botox' },
      { value: 'Fillers', label: 'Fillers' },
      { value: 'Aethoxysklerol', label: 'Aethoxysklerol' },
    ]
  },
  { 
    label: 'Lot No', 
    name: 'lot_no',
    type: 'data' 
  },
  {
    label: 'Units',
    name: 'units',
    type: 'select',
    options: [
      { value: '1u', label: '1u' },
      { value: '2u', label: '2u' },
      { value: '3u', label: '3u' },
    ]
  },
  {
    label: 'ML',
    name: 'ml',
    type: 'select',
    options: [
      { value: '2ml', label: '2ml' },
      { value: '3ml', label: '3ml' },
    ]
  },
]

const ExcalidrawWrapper = () => {
  const [index, setIndex] = useState(0);
  const [excalidrawAPI, setExcalidrawAPI] = useState(null);
  const [drawingsSidebar, setDrawingsSidebar] = useState(true);
  const [applicationSidebar, setApplicationSidebar] = useState(false);
  const [currentApp, setCurrentApp] = useState('')
  const [newElement, setNewElement] = useState('')
  const [selectedElement, setSelectedElement] = useState('')
  const [laserVars, setLaserVars] = useState({
    fluence: '',
    spot_size: '',
    pulse_duration: '',
    repetition_rate: '',
    no_of_pulses: '',
  })
  const [injectableVars, setInjectableVars] = useState({
    injectable: '',
    lot_no: '',
    units: '',
    ml: '',
  })
  const [images, setImages] = useState({
    male: [
      { name: '3D Face', src: MaleFace3D, id: '' },
      { name: '3D Body F&B', src: MaleBodyFB3d, id: '' },
      { name: 'Head', src: Head, id: '' },
      { name: 'Body', src: BodyMale, id: '' },
      { name: 'Body Male And Female', src: BodyMaleAndFemale, id: '' },
    ],
    female: [
      { name: 'Face & Scalp', src: FaceAndScalpFemale, id: '' },
      { name: 'Face1', src: FaceFemale1, id: '' },
      { name: 'Face2', src: FaceFemale2, id: '' },
      { name: 'Body', src: BodyFemale, id: '' },
      { name: 'Body Male And Female', src: BodyMaleAndFemale, id: '' },
    ],
  });

  useEffect(() => {
    if (excalidrawAPI) {
      // Register the global save function only after API is set
      window.ExcalidrawAPI = {
        saveCanvasAsImage: saveCanvasAsImage
      };
    }
  }, [excalidrawAPI]);

  const updateElementCustomData = (target, newVars) => {
    const sceneElements = excalidrawAPI.getSceneElements().map(element => {
      if(element.id === target.id){
        if(newVars)
          element.customData = newVars
        else if(currentApp === 'Laser')
          element.customData = {...laserVars, type: currentApp}
        else
          element.customData = {...injectableVars, type: currentApp}
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
    if(applicationSidebar && currentApp && appState.activeTool.type !== 'freedraw' && appState.activeTool.type !== 'selection' && !selectedElement){
      setCurrentApp('')
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
      console.log('New element added:', excalidrawAPI.getSceneElements());
    
      setNewElement(null)
    }
  };

  const handleExcaliPointerDown = (activeTool, pointerDownState) => {
    const thisElement = pointerDownState.hit.element;
    if (thisElement && thisElement.type === 'freedraw') {
      console.log('Element selected:', thisElement);
      if(thisElement.customData.type === 'Laser'){
        setLaserVars(thisElement.customData)
      }
      else{
        setInjectableVars(thisElement.customData)
      }
      setSelectedElement(thisElement)
      setCurrentApp(thisElement.customData.type)
    }
    else{
      if(activeTool.type === "selection"){
        setSelectedElement('')
        setCurrentApp('')
      }
    }
  };

  const handleDrawModeClick = (app) => {
    if (!excalidrawAPI) return;

    setCurrentApp(app.name);
    excalidrawAPI.updateScene({
      appState: {
        ...excalidrawAPI.getAppState(),
        activeTool: {
          type: "freedraw",
        },
        currentItemStrokeColor: app.color, // Set your desired stroke color here
      },
      commitToHistory: true,
    });
    // excalidrawAPI.scrollToContent()
    // excalidrawAPI.refresh()
  };

  const handleImageClick = async (img, array, gender) => {
    if (!excalidrawAPI) return;

    const canvasContainer = document.querySelector('.excalidraw__canvas'); // Assuming Excalidraw canvas has this class
    const canvasHeight = canvasContainer.clientHeight;
    const canvasWidth = canvasContainer.clientWidth;
  
    const image = new Image();
    image.src = img.src;
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
        const newArray = array.map(val => {
          if (val.src === img.src) val.id = fileId;
          return val;
        });
        setImages({ ...images, [gender]: newArray });
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
        id: img.name,
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

  const saveCanvasAsImage = async () => {
    try {
      if (!excalidrawAPI) {
        console.error('Excalidraw API not initialized');
        return;
      }
      const blob = await excalidrawAPI.exportToBlob({ mimeType: 'image/png' });
      const url = URL.createObjectURL(blob);

      // Call the Vue callback with the image URL
      if (setImageCallback) {
        setImageCallback(url);
      }

      console.log('Canvas saved as image');
    } catch (error) {
      console.error('Failed to save the canvas as an image:', error);
    }
  };

  return (
    <div style={{ height: '100%' }}>
      <div className={'excalidraw-wrapper ' + (currentApp ? 'leftdrawer-open' : '')} style={{ height: '100%', position: 'relative'}}>
        {currentApp && <Card variant='soft' sx={{ width: 240, zIndex: 10, marginTop: '40px', height: 'fit-content', position: 'absolute'}}>
          {currentApp === 'Laser' ? 
            LaserVariables.map((variable, index) => <div key={index}>
              <FormLabel>{variable.label}</FormLabel>
              {variable.type === 'select' ? 
                <Select 
                name={variable.name}
                isClearable
                value={variable.options.find(option => option.value === laserVars[variable.name]) || ''}
                onChange={(selectedOption) => {
                  const newVars = {
                    ...laserVars,
                    [variable.name]: selectedOption ? selectedOption.value : ''
                  }
                  setLaserVars(newVars);
                  if(selectedElement)
                    updateElementCustomData(selectedElement, newVars)
                }}
                options={variable.options}
                />
              : variable.type === 'data' ? <Input value={laserVars[variable.name]} onChange={event => {
                const newVars = {
                  ...laserVars,
                  [variable.name]: event.target.value
                }
                setLaserVars(newVars);
                if(selectedElement)
                  updateElementCustomData(selectedElement, newVars)
              }}/> 
            : <></>}</div>) :

            InjectableVars.map((variable, index) => <div key={index}>
            <FormLabel>{variable.label}</FormLabel>
            {variable.type === 'select' ? 
              <Select 
              name={variable.name}
              isClearable
              value={variable.options.find(option => option.value === injectableVars[variable.name]) || ''}
              onChange={(selectedOption) => {
                const newVars = {
                  ...injectableVars,
                  [variable.name]: selectedOption ? selectedOption.value : ''
                }
                setInjectableVars(newVars);
                if(selectedElement)
                  updateElementCustomData(selectedElement, newVars)
              }}
              options={variable.options}
              />

              : variable.type === 'data' ? <Input value={injectableVars[variable.name]} onChange={event => {
                const newVars = {
                  ...injectableVars,
                  [variable.name]: event.target.value
                }
                setInjectableVars(newVars);
                if(selectedElement)
                  updateElementCustomData(selectedElement, newVars)
              }}/> 
            : <></>}</div>)
          } 
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
              {!applicationSidebar && <Button 
              name="applications" 
              color="success" 
              variant="soft" 
              onClick={() => {excalidrawAPI.toggleSidebar({name: 'applications'})}}
              >
                Applications
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
                    <List>
                      {images.male.map((img, index, array) => (
                        <ListItemButton key={img.name} onClick={() => {handleImageClick(img, array, 'male')}}>
                          <ListItemDecorator>
                            <img src={img.src} alt={img.name} style={{ width: '50px', height: '50px', marginRight: '15px' }} />
                          </ListItemDecorator>
                          {img.name}
                        </ListItemButton>
                      ))}
                    </List>
                  </div>
                </TabPanel>
                <TabPanel value={1} sx={{ p: 0 }}>
                  <div>
                    <List>
                      {images.female.map((img, index, array) => (
                        <ListItemButton key={img.name} onClick={() => {handleImageClick(img, array, 'female')}}>
                          <ListItemDecorator>
                            <img src={img.src} alt={img.name} style={{ width: '50px', height: '50px', marginRight: '15px' }} />
                          </ListItemDecorator>
                          {img.name}
                        </ListItemButton>
                      ))}
                    </List>
                  </div>
                </TabPanel>
              </Tabs>
            </Sidebar.Tabs>
          </Sidebar>

          <Sidebar name="applications" className='applications-sidebar' docked onStateChange={setApplicationSidebar}>
            <RadioGroup
            overlay
            name="applications"
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
              {Applications.map((value, index) => (
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
                  <Radio id={value.name} value={value.name} checkedIcon={<CheckCircleRoundedIcon />}/>
                  {value.name}
                </Sheet>
              ))}
            </RadioGroup>
          </Sidebar>
        </Excalidraw>
      </div>
    </div>
  );
};

export default ExcalidrawWrapper;