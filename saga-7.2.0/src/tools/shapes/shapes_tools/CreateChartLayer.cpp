/**********************************************************
 * Version $Id$
 *********************************************************/
/*******************************************************************************
    CCreateChartLayer.cpp
    Copyright (C) Victor Olaya
    
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301, USA
*******************************************************************************/ 

///////////////////////////////////////////////////////////
//														 //
//														 //
//														 //
///////////////////////////////////////////////////////////

//---------------------------------------------------------
#include "CreateChartLayer.h"


///////////////////////////////////////////////////////////
//														 //
//														 //
//														 //
///////////////////////////////////////////////////////////

//---------------------------------------------------------
CCreateChartLayer::CCreateChartLayer(void)
{
	Set_Name		(_TL("Create Chart Layer (bars/sectors)"));

	Set_Author		("V.Olaya (c) 2004");

	Set_Description	(_TW(
		"(c) 2004 by Victor Olaya. "
	));
		
	Parameters.Add_Shapes("", 
		"INPUT", _TL("Shapes"), 
		_TL(""), 
		PARAMETER_INPUT
	);

	Parameters.Add_Table_Field("INPUT",
		"SIZE", _TL("Size field"),
		_TL("")
	);

	Parameters.Add_Double("", 
		"MAXSIZE", _TL("Maximum size"), 
		_TL(""),
		100, 0, true
	);

	Parameters.Add_Double("", 
		"MINSIZE", _TL("Minimum size"), 
		_TL(""),
		10, 0, true
	);
	
	Parameters.Add_Choice("", 
		"TYPE", _TL("Type"), 
		_TL(""), 
		CSG_String::Format("%s|%s|",
			_TL("Sectors"),
			_TL("Bars|")
		), 0
	);

	Add_Parameters("EXTRA", _TL("Fields for diagram"), _TL(""));
}


///////////////////////////////////////////////////////////
//														 //
///////////////////////////////////////////////////////////

//---------------------------------------------------------
bool CCreateChartLayer::On_Execute(void)
{	
	CSG_Shapes *pInput;
	int i=0;
	int iType;	
	int iSizeField;
	
	if( GetExtraParameters() )
	{

		iSizeField = Parameters("SIZE")->asInt();
		m_fMaxSize = (double) Parameters("MAXSIZE")->asDouble();
		m_fMinSize = (double) Parameters("MINSIZE")->asDouble();

		if (m_fMinSize > m_fMaxSize){
			m_fMinSize = m_fMaxSize;
		}//if

		iType = Parameters("TYPE")->asInt();
		pInput = Parameters("INPUT")->asShapes();
		m_fMaxValue = pInput->Get_Maximum(iSizeField);
		m_fMinValue = pInput->Get_Minimum(iSizeField);

		switch( iType)
		{
		default:
			m_pOutput = SG_Create_Shapes(SHAPE_TYPE_Polygon, _TL("Chart (sectors):"));
			break;

		case  1:
			m_pOutput = SG_Create_Shapes(SHAPE_TYPE_Polygon, _TL("Chart (bars):"));
			break;
		}

		m_pOutput->Add_Field(_TL("Field (ID)"), SG_DATATYPE_Int);
		m_pOutput->Add_Field(_TL("Field (Name)"), SG_DATATYPE_String);


		for (i = 0; i < pInput->Get_Count(); i++)
		{
			switch( iType)
			{
			default:
				AddPieChart(pInput->Get_Shape(i),pInput->Get_Type());
				break;

			case  1:
				AddBarChart(pInput->Get_Shape(i),pInput->Get_Type());
				break;
			}
		}
		
		DataObject_Add(m_pOutput, false);

		delete [] m_bIncludeParam;
		
		return true;
	}//if

	delete [] m_bIncludeParam;

	return false;
}//method


///////////////////////////////////////////////////////////
//														 //
///////////////////////////////////////////////////////////

//---------------------------------------------------------
bool CCreateChartLayer::GetExtraParameters(void)
{
	int		i;
	CSG_Shapes *pInput = Parameters("INPUT")->asShapes();

	CSG_Parameters	*pParameters	= Get_Parameters("EXTRA");
	
	pParameters->Create(this, _TL("Fields for diagram"), _TL(""), SG_T("EXTRA"));

	m_bIncludeParam = new bool [pInput->Get_Field_Count() ];

	for(i=0; i<pInput->Get_Field_Count(); i++)
	{
		if( SG_Data_Type_is_Numeric(pInput->Get_Field_Type(i)) )
		{
			pParameters->Add_Bool("", SG_Get_String(i), pInput->Get_Field_Name(i), _TL(""), false);
		}
	}

	bool bIsValidSelection = false;

	if( Dlg_Parameters("EXTRA") )
	{
		for(i=0; i<pInput->Get_Field_Count(); i++)
		{
			CSG_Parameter	*pParameter	= Get_Parameters("EXTRA")->Get_Parameter(SG_Get_String(i));

			if( pParameter )
			{
				m_bIncludeParam[i]	= pParameter->asBool();
				bIsValidSelection	= true;
			}//try
			else
			{
				m_bIncludeParam[i]	= false;
			}//else
		}//for
	}//if

	pParameters->Destroy();

	return bIsValidSelection;
}//method


///////////////////////////////////////////////////////////
//														 //
///////////////////////////////////////////////////////////

//---------------------------------------------------------
void CCreateChartLayer::AddPieChart(CSG_Shape *pShape, int iType)
{
	int i,j;
	int iSteps;
	int iSizeField;
	int iField;
	double fSum = 0;
	double fPartialSum = 0;
	double fSize;	
	double fSectorSize;
	double dX, dY;
	CSG_Shape *pSector;
	CSG_Table_Record *pRecord;
	TSG_Point Point;
		
	iSizeField = Parameters("SIZE")->asInt();

	pRecord = pShape;
	for (i = 0; i < pRecord->Get_Table()->Get_Field_Count(); i++){
		if (m_bIncludeParam[i]){
			fSum += pRecord->asFloat(i);
		}//if
	}//for

	fSize = pRecord->asFloat(iSizeField);
	fSize = m_fMinSize + (m_fMaxSize - m_fMinSize)/(m_fMaxValue - m_fMinValue) * (fSize - m_fMinValue);

	switch (iType){
	case SHAPE_TYPE_Polygon:
		Point = ((CSG_Shape_Polygon*) pShape)->Get_Centroid();	
		break;
	case SHAPE_TYPE_Line:
		Point = GetLineMidPoint((CSG_Shape_Line*)pShape);
		break;
	case SHAPE_TYPE_Point:
		Point = pShape->Get_Point(0);
		break;
	default:
		break;
	}//switch
	dX = Point.x;
	dY = Point.y;

	fPartialSum = 0;
	iField = 1;
	for (i = 0; i < pRecord->Get_Table()->Get_Field_Count(); i++){
		if (m_bIncludeParam[i]){
			fSectorSize = pRecord->asFloat(i) / fSum;
			pSector = m_pOutput->Add_Shape();
			pSector->Add_Point(dX,dY);
			iSteps = (int) (fSectorSize * 200.);
			for (j = 0; j < iSteps; j++){
				pSector->Add_Point(dX + fSize * sin((fPartialSum + (double)j / 200.) * M_PI_360),
									dY + fSize * cos((fPartialSum + (double)j / 200.) * M_PI_360));
			}//for
			fPartialSum +=fSectorSize;
			pSector->Add_Point(dX + fSize * sin(fPartialSum * M_PI_360),
								dY + fSize * cos(fPartialSum * M_PI_360));		
			pSector->Set_Value(0,iField);
			pSector->Set_Value(1,pRecord->Get_Table()->Get_Field_Name(i));
			iField++;
		}//if
	}//for

}//method


///////////////////////////////////////////////////////////
//														 //
///////////////////////////////////////////////////////////

//---------------------------------------------------------
void CCreateChartLayer::AddBarChart(CSG_Shape* pShape, int iType)
{
	int i;
	int iSizeField;
	int iField;
	int iValidFields = 0;
	double fMax;	
	double fMin;
	double fSize;	
	double fBarHeight, fBarWidth;
	double dX, dY;
	CSG_Shape *pSector;
	CSG_Table_Record *pRecord;
	TSG_Point Point;
		
	iSizeField = Parameters("SIZE")->asInt();
	pRecord = pShape;

	pRecord = pShape;
	for (i = 0; i < pRecord->Get_Table()->Get_Field_Count(); i++){
		if (m_bIncludeParam[i]){
			if (!iValidFields){
				fMin = fMax = pRecord->asFloat(i);
			}
			else{					
				if (pRecord->asFloat(i) > fMax){
					fMax = pRecord->asFloat(i);
				}//if
				if (pRecord->asFloat(i) < fMin){
					fMin = pRecord->asFloat(i);
				}//if
			}//else
			iValidFields++;
		}//if
	}//for

	if (fMax > 0 && fMin > 0){
		fMin = 0;
	}//if

	if (fMax < 0 && fMin < 0){
		fMax = 0;
	}//if
	fSize = pRecord->asFloat(iSizeField);
	fSize = m_fMinSize + (m_fMaxSize - m_fMinSize)/(m_fMaxValue - m_fMinValue) * (fSize - m_fMinValue);

	switch (iType){
	case SHAPE_TYPE_Polygon:
		Point = ((CSG_Shape_Polygon*) pShape)->Get_Centroid();	
		break;
	case SHAPE_TYPE_Line:
		Point = GetLineMidPoint((CSG_Shape_Line*)pShape);
		break;
	case SHAPE_TYPE_Point:
		Point = pShape->Get_Point(0);
		break;
	default:
		break;
	}//switch
	dX = Point.x;
	dY = Point.y;
	
	fBarWidth = fSize / (double)iValidFields;

	iField = 1;
	for (i = 0; i < pRecord->Get_Table()->Get_Field_Count(); i++){
		if (m_bIncludeParam[i]){
			fBarHeight = pRecord->asFloat(i) / (fMax - fMin) * fSize;
			pSector = m_pOutput->Add_Shape();
			pSector->Add_Point(dX - fSize / 2. + fBarWidth * (iField - 1) ,
								dY);
			pSector->Add_Point(dX - fSize / 2. + fBarWidth * iField,
								dY);
			pSector->Add_Point(dX - fSize / 2. + fBarWidth * iField,
								dY + fBarHeight);
			pSector->Add_Point(dX - fSize / 2. + fBarWidth * (iField - 1) ,
								dY + fBarHeight);
			pSector->Set_Value(0,iField);
			pSector->Set_Value(1,pRecord->Get_Table()->Get_Field_Name(i));
			iField++;
		}//if
	}//for
}


///////////////////////////////////////////////////////////
//														 //
///////////////////////////////////////////////////////////

//---------------------------------------------------------
TSG_Point CCreateChartLayer::GetLineMidPoint(CSG_Shape_Line *pLine)
{
	int i;
	double fDist, fAccDist = 0;
	double fLength = pLine->Get_Length(0) / 2.;
	TSG_Point Point, Point2, ReturnPoint;

	for (i = 0; i < pLine->Get_Point_Count(0) - 1; i++){
		Point = pLine->Get_Point(i);
		Point2 = pLine->Get_Point(i+1);
		fDist = sqrt(pow(Point.x - Point2.x,2.) + pow(Point.y - Point2.y,2.));
		if (fAccDist <= fLength && fAccDist + fDist > fLength){
			ReturnPoint.x = Point.x + (Point2.x - Point.x) * (fLength - fAccDist) / fDist;
			ReturnPoint.y = Point.y + (Point2.y - Point.y) * (fLength - fAccDist) / fDist;
			return ReturnPoint;
		}//if
		fAccDist += fDist;
	}//for

	return pLine->Get_Point(pLine->Get_Point_Count(0) / 2);
}


///////////////////////////////////////////////////////////
//														 //
//														 //
//														 //
///////////////////////////////////////////////////////////

//---------------------------------------------------------
