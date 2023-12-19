import React, {useState} from "react";
import styled from "styled-components";

interface ClubProps {
    name: string;
    description: string;
    // children?: React.ReactNode; // 👈️ for demo purposes
}

function ListBox(props: ClubProps) {
    const [isToggled, setToggled] = useState<boolean>(false)
    return(
        <ListBoxArea onClick={()=>setToggled(!isToggled)}>
            <NameArea>{props.name}</NameArea>
            {(isToggled) &&
                (<DescriptionArea>{props.description}</DescriptionArea>)}
        </ListBoxArea>
    )
}

export default ListBox;

const ListBoxArea = styled.div`
  width: 297px;
  margin-bottom: 12px;
  flex-shrink: 0;
  border-radius: 16px;
  background: #F3F4FF;
  filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
`

const NameArea = styled.div`
  width: 195px;
  height: 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  
  color: #201276;

  text-align: center;
  //font-family: Roboto Mono;
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: 16px; /* 80% */
  letter-spacing: 0.1px;
`

const DescriptionArea = styled.div`
  width: 269px;
  margin-top: 10px;
  margin-bottom: 12px;
  
  color: #201276;
  background: #FFF;
  text-align: center;
  //font-family: Roboto Mono;
  font-size: 15px;
  font-style: normal;
  font-weight: 400;
  line-height: 25px; /* 166.667% */
  letter-spacing: 0.075px;
    
`